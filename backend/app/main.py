import asyncio

import uvicorn
from fastapi import FastAPI

# from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from app import config
from app.api import route
from app.database import database

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    docs_url=config.PROJECT_DOCS_URL,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route.router, prefix=config.PROJECT_API_V1_URL)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
