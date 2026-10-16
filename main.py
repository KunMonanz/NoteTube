from fastapi import FastAPI

from v1.router import router as transcribe_router

app = FastAPI(title="NoteTube")

app.include_router(transcribe_router)
