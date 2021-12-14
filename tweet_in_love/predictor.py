"""Predictors are instances of trained models.
This module implements the process of loading a model
and generate a usable prediction.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

import spacy
from pydantic import BaseModel
from spacy.language import Language


class PredictorInterface(ABC):
    @abstractmethod
    def predict(self, items: List[str]) -> List[str]:
        pass

    def predict_one(self, item: str) -> str:
        return self.predict([item])[0]


class SpacyPredictor(BaseModel, PredictorInterface):
    model: Language

    @classmethod
    def load(cls, model_path: Path):
        nlp = spacy.load(model_path)
        return cls(model=nlp)

    def predict(self, items: List[str]) -> List[str]:
        # predict for all
        docs = self.model.pipe(items)
        # extract prediction dicts
        cats: List[Dict[str, float]] = [doc.cats for doc in docs]
        # get the keys with the maximum value for each item
        preds = [max(cat, key=cat.get) for cat in cats]  # type:ignore
        return preds

    class Config:
        arbitrary_types_allowed = True
