"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Health route
"""
from fastapi import APIRouter

from app.data_models.heartbeat import HearbeatResult

router = APIRouter()


@router.get("/heartbeat", response_model=HearbeatResult, name="heartbeat")
def get_hearbeat() -> HearbeatResult:
    heartbeat = HearbeatResult(is_alive=True)
    return heartbeat
