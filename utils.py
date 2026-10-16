import urllib.parse as urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def fetch_youtube_transcript(video_id: str):
    try:
        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

        full_text = " ".join([segment["text"] for segment in raw_transcript])

        return {"status": "success", "video_id": video_id, "transcript": full_text}

    except Exception as e:
        return {"status": "error", "message": str(e)}
