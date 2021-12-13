from typing import Optional

from tweet_in_love.settings import GlobalSettings

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

# load .env
load_dotenv(find_dotenv())

settings = GlobalSettings()

app = FastAPI(
    title=settings.project_name, debug=settings.debug, version=settings.version
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False, debug=False)
