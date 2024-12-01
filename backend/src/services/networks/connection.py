from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .configNw import origins

def connect_networks(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app