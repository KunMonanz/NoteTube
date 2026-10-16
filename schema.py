import re

from pydantic import BaseModel, HttpUrl, computed_field, field_validator


class GeminiResponse(BaseModel):
    response: str


class GeminiResponseError(BaseModel):
    message: str


class TranscribeRequest(BaseModel):
    url: HttpUrl

    @field_validator("url", mode="before")
    @classmethod
    def standardize_youtube_url(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("URL must be a valid string")
        url_str = value.strip()

        youtube_regex = (
            r"(?:https?:\/\/)?(?:www\.|m\.)?"
            r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?|shorts)\/|\S*?[?&]v=)|youtu\.be\/)"
            r"([a-zA-Z0-9_-]{11})"
        )

        match = re.search(youtube_regex, url_str)

        if not match:
            raise ValueError("Not a valid YouTube video URL")

        video_id = match.group(1)

        return f"https://youtube.com{video_id}"

    @computed_field
    @property
    def video_id(self) -> str:
        """Extracts and exposes the exact video ID automatically."""
        query_string = self.url.query
        if query_string and "v=" in query_string:
            return query_string.split("v=")[1][:11]
        return ""


class TranscribeResponseSuccess(BaseModel):
    status: str = "success"
    video_id: str
    full_text: str


class TranscribeResponseFail(BaseModel):
    status: str = "failed"
    message: str
