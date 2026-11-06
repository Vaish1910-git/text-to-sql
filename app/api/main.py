from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.engine.text_to_sql import generate_sql
from app.engine.clarification import detect_ambiguity
from app.engine.sql_corrector import generate_valid_sql
from app.database.connection import execute_query


app = FastAPI(
    title="Text-to-SQL AI",
    description="Convert natural language questions into SQL queries.",
    version="1.0.0"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str


class ClarificationRequest(BaseModel):
    original_question: str
    selected_option: str


def process_question(question):

    # Step 1: Generate SQL
    initial_sql = generate_sql(question)

    # Step 2: Validate and correct SQL
    sql_query, is_valid, message = generate_valid_sql(
        question, initial_sql
    )

    if not is_valid:
        return {
            "status": "error",
            "generated_sql": sql_query,
            "message": message
        }

    # Step 3: Execute SQL
    results = execute_query(sql_query)

    return {
        "status": "success",
        "question": question,
        "generated_sql": sql_query,
        "validation_message": message,
        "results": results
    }


@app.get("/")
def home():
    return {
        "message": "Text-to-SQL AI API is running!"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Step 1: Detect ambiguity
    clarification = detect_ambiguity(request.question)

    if clarification["is_ambiguous"]:
        return {
            "status": "clarification_required",
            "original_question": request.question,
            "clarification_question": clarification["question"],
            "options": clarification["options"]
        }

    # Step 2: Process clear question
    return process_question(request.question)


@app.post("/clarify")
def clarify_question(request: ClarificationRequest):

    # Recheck the original question
    clarification = detect_ambiguity(request.original_question)

    if not clarification["is_ambiguous"]:
        raise HTTPException(
            status_code=400,
            detail="This question does not require clarification."
        )

    # Validate selected option
    if request.selected_option not in clarification["options"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid clarification option."
        )

    # Combine original question and selected meaning
    clarified_question = (
        f"Original question: {request.original_question}\n"
        f"Clarified meaning: {request.selected_option}"
    )

    return process_question(clarified_question)