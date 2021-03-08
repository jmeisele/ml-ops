"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Main entry point for FastAPI app
"""
from app.api.routes.router import api_router
from app.core.config import API_PREFIX, APP_NAME, APP_VERSION, IS_DEBUG
from app.core.event_handlers import start_app_handler, stop_app_handler
from app.core.monitoring import instrumentator

from fastapi import FastAPI


def get_app() -> FastAPI:
    """FastAPI app controller"""
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    instrumentator.instrument(fast_app).expose(fast_app, include_in_schema=False, should_gzip=True)
    fast_app.include_router(api_router, prefix=API_PREFIX)
    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))
    return fast_app


app = get_app()
