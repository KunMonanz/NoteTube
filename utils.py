import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from youtube_transcript_api import YouTubeTranscriptApi

from schema import TranscribeResponseFail, TranscribeResponseSuccess

executor = ThreadPoolExecutor(max_workers=10)

logger = logging.getLogger(__name__)


def _blocking_youtube_fetch(video_id: str):
    """Internal blocking client execution context wrapper."""
    raw_transcript = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
    return " ".join([segment.text for segment in raw_transcript])


async def fetch_youtube_transcript(video_id: str):
    logger.info("Attempting to transcribe YouTube video of video_id: %s", video_id)
    try:
        loop = asyncio.get_running_loop()
        full_text = await loop.run_in_executor(
            executor, _blocking_youtube_fetch, video_id
        )
        logger.info("Successfully transcribed YouTube video of video_id: %s", video_id)
        return TranscribeResponseSuccess(video_id=video_id, transcript=full_text)

    except Exception as e:
        logger.exception("Failed to transcribe YouTube video: %s", str(e))
        return TranscribeResponseFail(message=str(e), video_id=video_id)
