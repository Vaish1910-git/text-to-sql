
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt):

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

            else:
                raise


if __name__ == "__main__":

    try:
        answer = ask_gemini(
            "Explain what SQL is in two simple sentences."
        )

        print("\nGemini response:")
        print(answer)

    except Exception as e:
        print("Gemini API error:", e)
