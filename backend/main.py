import uvicorn

from cfg import settings
from src import app

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT
    )
