from typing import Union
from fastapi import FastAPI

from routes import index
from routes.api import detect

app = FastAPI()

app.include_router(index.router)
app.include_router(detect.router, prefix="/api")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
