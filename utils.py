import urllib.parse as urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url):
    """Helper to extract the video ID from various YouTube URL formats."""
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    if "v" in query:
        return query["v"][0]
    return url_data.path.split("/")[-1]


def fetch_youtube_transcript(video_url: str):
    try:
        video_id = get_video_id(video_url)

        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

        full_text = " ".join([segment["text"] for segment in raw_transcript])

        return {"status": "success", "video_id": video_id, "transcript": full_text}

    except Exception as e:
        return {"status": "error", "message": str(e)}
