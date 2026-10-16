import logging
import os

from dotenv import load_dotenv
from google import genai

from schema import GeminiResponse, GeminiResponseError

load_dotenv()
logger = logging.getLogger(__name__)


def get_gemini_response() -> GeminiResponse | GeminiResponseError:
    try:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Explain quantum computing in one simple sentence.",
        )

        response_text = response.text

        if not response_text:
            logger.exception("Error in gemini response: response returns None")
            return GeminiResponseError(message="Error in gemini response")
        return GeminiResponse(response=response_text)

    except Exception as e:
        logger.exception("Error in gemini response: %s", str(e))
        return GeminiResponseError(message="Error in gemini response")
