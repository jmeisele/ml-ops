"""
Author: Jason Eisele
Date: December 2, 2020
Scope: ML Model objects handling pre/post processing along with predictions
"""
from typing import List
from random import randint

import joblib
import numpy as np
from loguru import logger

from app.core.messages import NO_VALID_PAYLOAD
from app.data_models.payload import HousePredictionPayload, payload_to_list
from app.data_models.prediction import HousePredictionResult


class HousePriceModel(object):

    RESULT_UNIT_FACTOR = 100000

    def __init__(self, path):
        self.path = path
        self._load_local_model()
        self.version = "A"

    def _load_local_model(self):
        self.model = joblib.load(self.path)

    def _pre_process(self, payload: HousePredictionPayload) -> List:
        logger.info("Pre-processing payload.")
        result = np.asarray(payload_to_list(payload)).reshape(1, -1)
        return result

    def _post_process(self, prediction: np.ndarray) -> HousePredictionResult:
        logger.info("Post-processing prediction.")
        result = prediction.tolist()
        human_readable_unit = result[0] * self.RESULT_UNIT_FACTOR
        hpp = HousePredictionResult(median_house_value=human_readable_unit)
        return hpp

    def _predict(self, features: List) -> np.ndarray:
        logger.info("Predicting.")
        prediction_result = self.model.predict(features)
        return prediction_result + float(randint(1, 20))

    def predict(self, payload: HousePredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))
        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logger.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result
