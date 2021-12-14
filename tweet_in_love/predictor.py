"""
Predictors are instances of trained models.

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
    """
    A generic interface for the predictors
    """

    @abstractmethod
    def predict(self, items: List[str]) -> List[str]:
        """
        Return model predictions for a list of items

        Parameters
        ----------
        items : List[str]
            a list of string to predict

        Returns
        -------
        List[str]
            the list of predicted classes
        """

    def predict_one(self, item: str) -> str:
        """
        Return predictions for a single item

        Parameters
        ----------
        item : str
            The string to predict

        Returns
        -------
        str
            the predicted class
        """
        return self.predict([item])[0]


class SpacyPredictor(BaseModel, PredictorInterface):
    """
    A Predictor for Spacy Language models
    """

    model: Language

    @classmethod
    def load(cls, model_path: Path):
        """
        Factory method to generate a SpacyPredictor instance.

        Parameters
        ----------
        model_path : Path
            Path to the model to use for the predictions
        """
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
