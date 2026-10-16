import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_gemini_response():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain quantum computing in one simple sentence.",
    )

    return {"response": response.text}
