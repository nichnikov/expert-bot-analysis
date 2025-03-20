from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Настройки приложения, включая параметры Elasticsearch."""
    api_key: str
    api_host: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Parameters(BaseModel):
    """Параметры приложения, включая параметры Elasticsearch и модели."""
    prompt: str = ""
    max_tokens: int = 3000
    temperature: float = 0.2
    data_file_name: str = ""
