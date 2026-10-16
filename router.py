from fastapi import APIRouter, Request, Response, status
from fastapi.exceptions import HTTPException

from gemini import get_gemini_response
from ratelimiting import check_ip_rate_limit
from schema import GeminiResponseError, TranscribeRequest, TranscribeResponseSuccess
from utils import fetch_youtube_transcript

router = APIRouter(prefix="/api/v1/transcribes")


@router.post("/", status_code=status.HTTP_200_OK)
async def transcribe_and_export_markdown(payload: TranscribeRequest, request: Request):
    await check_ip_rate_limit(request)

    video_id = payload.video_id

    youtube_transcript = await fetch_youtube_transcript(video_id)

    if not isinstance(youtube_transcript, TranscribeResponseSuccess):
        return Response(
            content="Failed to retrieve video transcript",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    gemini_result = await get_gemini_response(youtube_transcript.transcript)
    if isinstance(gemini_result, GeminiResponseError):
        return gemini_result

    file_content = gemini_result.response
    file_name = f"notes_{video_id}.md"

    return Response(
        content=file_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )
