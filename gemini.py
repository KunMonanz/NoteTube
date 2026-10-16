import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from schema import GeminiResponse, GeminiResponseError

load_dotenv()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


async def get_gemini_response(
    transcript_text: str,
) -> GeminiResponse | GeminiResponseError:
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=gemini_api_key)

        template_path = BASE_DIR / "prompt_template.txt"
        with open(template_path, "r", encoding="utf-8") as file:
            user_prompt_template = file.read()

        system_instruction_path = BASE_DIR / "system_prompt.txt"
        with open(system_instruction_path, "r", encoding="utf-8") as file:
            system_instruction = file.read()

        formatted_contents = user_prompt_template.format(
            transcript_text=transcript_text
        )

        max_retries = 3
        base_delay = 2

        for attempt in range(max_retries):
            try:
                response = await client.aio.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                        max_output_tokens=1500,
                    ),
                )

                response_text = response.text
                if not response_text:
                    logger.exception("Error in gemini response: response returns None")
                    return GeminiResponseError(
                        message="Error in gemini response: Empty payload"
                    )

                return GeminiResponse(response=response_text)

            except APIError as api_err:
                if api_err.code in [503, 429] and attempt < max_retries - 1:
                    sleep_time = base_delay * (2**attempt)
                    logger.warning(
                        f"Gemini API busy ({api_err.code}). Retrying in {sleep_time}s... (Attempt {attempt + 1}/{max_retries})"
                    )
                    await asyncio.sleep(sleep_time)
                    continue

                logger.error(
                    f"Gemini API failed permanently with status {api_err.code}: {api_err.message}"
                )
                return GeminiResponseError(
                    message=f"Gemini API error: {api_err.message}"
                )

    except Exception as e:
        logger.exception("Error in gemini response: %s", str(e))
        return GeminiResponseError(message=f"Gemini API error: {str(e)}")
