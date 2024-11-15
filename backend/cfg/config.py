from pydantic_settings import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = "Yolo11_Cars_Tracking"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class Settings(CommonSettings, ServerSettings):
    pass
