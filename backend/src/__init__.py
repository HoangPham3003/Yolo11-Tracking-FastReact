import os

from fastapi import FastAPI

from .endpoints import home
from .services.networks.connection import connect_networks

app = FastAPI(
    title = "Cars tracking",
    description="This is a fancy app for cars counting",
)

app = connect_networks(app)
app.include_router(home.router)