"""Main API controller."""

from fastapi import Depends, FastAPI
from src.api.routers import dependencies as dp
from src.api.routers import files
from starlette.middleware.cors import CORSMiddleware

APP = FastAPI(title="Dataset API", dependencies=[Depends(dp.get_api_key)])
APP.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_credentials=True
)

APP.include_router(files.router)
