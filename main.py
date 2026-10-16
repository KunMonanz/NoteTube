from fastapi import FastAPI

from logging_config import setup_logging
from v1.router import router as transcribe_router

setup_logging()

app = FastAPI(title="NoteTube")

app.include_router(transcribe_router)
