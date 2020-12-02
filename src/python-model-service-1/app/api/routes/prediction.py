"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Prediction route responsding to POST requests w/ background task
"""
from fastapi import APIRouter, BackgroundTasks
from starlette.requests import Request

# Incoming payload data model
from app.data_models.payload import HousePredictionPayload

# Outbound prediction result data model
from app.data_models.prediction import HousePredictionResult

# ML Model object itself
from app.services.models import HousePriceModel

# Background task
from app.api.tasks.queue import add_message_to_queue

router = APIRouter()

@router.post("/predict", response_model=HousePredictionResult, name="predict")
def post_predict(
    request: Request,
    backgound_tasks: BackgroundTasks,
    block_data: HousePredictionPayload = None,
) -> HousePredictionResult:
    model: HousePriceModel = request.app.state.model
    prediction: HousePredictionResult = model.predict(block_data)
    # backgound_tasks.add_task(add_message_to_queue, *args)
    return prediction
