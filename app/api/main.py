
import re

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.engine.text_to_sql import generate_sql
from app.engine.clarification import detect_ambiguity
from app.engine.sql_corrector import generate_valid_sql
from app.database.connection import execute_query


app = FastAPI(
    title="Text-to-SQL AI",
    description="Convert natural language questions into SQL queries.",
    version="1.0.0"
)


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


# Request models

class QuestionRequest(BaseModel):
    question: str


class ClarificationRequest(BaseModel):
    original_question: str
    selected_option: str | None = None
    custom_meaning: str | None = None


# Global exception handler

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print("Application error:", str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Something went wrong. Please try again."
        }
    )


# Check for unsupported write requests

def is_unsupported_write_request(question):
    patterns = [
        r"(?:^|;)\s*(please\s+)?(delete|remove|drop|truncate|update|modify|insert|alter)\b",
        r"(?:^|;)\s*(can|could|would)\s+you\s+(please\s+)?(delete|remove|drop|truncate|update|modify|insert|alter)\b",
        r"(?:^|;)\s*(i\s+)?(want|need)\s+to\s+(delete|remove|drop|truncate|update|modify|insert|alter)\b",
    ]

    return any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in patterns
    )


# Gemini error handler

def handle_gemini_error(error):
    error_message = str(error)

    if "503" in error_message or "UNAVAILABLE" in error_message:
        return {
            "status": "error",
            "message": (
                "Gemini service is temporarily unavailable. "
                "Please try again in a few moments."
            )
        }

    return {
        "status": "error",
        "message": (
            "Unable to process your question right now. "
            "Please try again."
        )
    }


# Common function to generate and execute SQL

def process_question(question):

    # Generate SQL using Gemini

    try:
        initial_sql = generate_sql(question)

    except Exception as e:
        print("SQL generation error:", str(e))
        return handle_gemini_error(e)

    # Validate and correct SQL

    try:
        sql_query, is_valid, message = generate_valid_sql(
            question,
            initial_sql
        )

    except Exception as e:
        print("SQL validation/correction error:", str(e))

        return {
            "status": "error",
            "message": (
                "Unable to validate or correct the generated SQL. "
                "Please try again."
            )
        }

    if not is_valid:
        return {
            "status": "error",
            "generated_sql": sql_query,
            "message": message
        }

    # Execute SQL in PostgreSQL

    try:
        results = execute_query(sql_query)

    except Exception as e:
        print("Database execution error:", str(e))

        return {
            "status": "error",
            "generated_sql": sql_query,
            "message": (
                "Unable to execute the SQL query. "
                "Please check the database connection and try again."
            )
        }

    return {
        "status": "success",
        "question": question,
        "generated_sql": sql_query,
        "validation_message": message,
        "results": results
    }


# Home endpoint

@app.get("/")
def home():
    return {
        "message": "Text-to-SQL AI API is running!"
    }


# Ask endpoint

@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Reject unsupported write operations

    if is_unsupported_write_request(request.question):
        return {
            "status": "rejected",
            "message": (
                "This operation is not supported. "
                "Text-to-SQL AI only supports read-only SELECT queries."
            )
        }

    # Detect ambiguity

    try:
        clarification = detect_ambiguity(request.question)

    except Exception as e:
        print("Ambiguity detection error:", str(e))
        return handle_gemini_error(e)

    if clarification["is_ambiguous"]:
        return {
            "status": "clarification_required",
            "original_question": request.question,
            "clarification_question": clarification["question"],
            "options": clarification["options"]
        }

    return process_question(request.question)


# Clarification endpoint

@app.post("/clarify")
def clarify_question(request: ClarificationRequest):

    if not request.original_question.strip():
        raise HTTPException(
            status_code=400,
            detail="Original question cannot be empty."
        )

    # Reject unsupported write operations

    if (
        is_unsupported_write_request(request.original_question)
        or (
            request.custom_meaning
            and is_unsupported_write_request(request.custom_meaning)
        )
        or (
            request.selected_option
            and is_unsupported_write_request(request.selected_option)
        )
    ):
        return {
            "status": "rejected",
            "message": (
                "This operation is not supported. "
                "Text-to-SQL AI only supports read-only SELECT queries."
            )
        }

    # User cannot provide both options and custom meaning

    if (
        request.selected_option is not None
        and request.custom_meaning is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="Provide either a selected option or custom meaning, not both."
        )

    # Get selected option or custom meaning

    if request.selected_option is not None:
        clarified_meaning = request.selected_option.strip()

    elif request.custom_meaning and request.custom_meaning.strip():
        clarified_meaning = request.custom_meaning.strip()

    else:
        raise HTTPException(
            status_code=400,
            detail="Please select an option or enter your own meaning."
        )

    if not clarified_meaning:
        raise HTTPException(
            status_code=400,
            detail="Clarification cannot be empty."
        )

    clarified_question = (
        f"Original question: {request.original_question}\n"
        f"Clarified meaning: {clarified_meaning}"
    )

    return process_question(clarified_question)
