from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Nexus Backend"
    VERSION: str = "1.0.0"

settings = Settings()
