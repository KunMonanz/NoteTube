from pydantic import BaseModel


class GeminiResponse(BaseModel):
    response: str


class GeminiResponseError(BaseModel):
    message: str
