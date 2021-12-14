from typing import List

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from tweet_in_love import __version__
from tweet_in_love.predictor import PredictorInterface, SpacyPredictor
from tweet_in_love.settings import DeployedModelSettings, GlobalSettings

from .io import Sentiment, Tweet

settings = GlobalSettings()
model_settings = DeployedModelSettings()
clf: PredictorInterface = SpacyPredictor.load(model_settings.model_best)

app = FastAPI(title=settings.project_name, version=__version__)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post("/predict_one", response_model=Sentiment)
async def predict_one(item: Tweet) -> Sentiment:
    pred = clf.predict_one(item.body)
    return Sentiment(prediction=pred)


@app.post("/predict_batch")
async def predict_batch(items: List[Tweet]) -> List[Sentiment]:
    txts = [item.body for item in items]
    preds = clf.predict(txts)
    return [Sentiment(prediction=pred) for pred in preds]
