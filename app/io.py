from pydantic import BaseModel


class Tweet(BaseModel):
    body: str


class Sentiment(BaseModel):
    prediction: str
