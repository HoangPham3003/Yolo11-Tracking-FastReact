import cv2

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..routers import api

router = APIRouter()
@router.get('/')
async def home():
    
    cap = cv2.VideoCapture("./DATA/CarsInHighway_mini.mp4")
    return StreamingResponse(api.stream_video(cap), media_type="text/event-stream")