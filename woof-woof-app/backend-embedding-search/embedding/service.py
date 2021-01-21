from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from embedding.routers import search
import embedding.utils as embedding_utils

prefix = "/v1"

# Setup FastAPI app
app = FastAPI(
    title="Embedding Server",
    description="Embedding Server",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception hooks

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc)
        }
    )

# Application start/stop hooks

@app.on_event("startup")
async def startup():
    #embedding_utils.ensure_data_loaded()
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

# Routes
@app.get(
    "/",
    summary="Index",
    description="Root api"
)
async def get_index():
    return {
        "message": "Welcome to the Embedding Server"
    }

# Additional routers here
#app.include_router(search.router, prefix=prefix)