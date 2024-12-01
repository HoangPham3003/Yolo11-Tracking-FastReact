import cv2
from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from ..routers import api


""" Test server-sent events (SSE)
async def fake_data_streamer():
    for i in range(10):
        msg = os.getenv("FASTAPI_APP_API_URL", "http://localhost:3000")
        message = f"{msg}"
        data = json.dumps(message)
        yield f'data: {data}\n\n'
        await asyncio.sleep(0.5)
"""

router = APIRouter()
@router.get('/')
async def home():
    # return StreamingResponse(fake_data_streamer(), media_type='text/event-stream')
    cap = cv2.VideoCapture("./DATA/CarsInHighway_mini.mp4")
    return StreamingResponse(api.stream_video(cap), media_type="text/event-stream", )
    
@router.get('/favicon.ico')
async def favicon():
    return status.HTTP_200_OK