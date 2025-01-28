from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import index
from routes.api import detect

app = FastAPI()

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router)
app.include_router(detect.router, prefix="/api")
