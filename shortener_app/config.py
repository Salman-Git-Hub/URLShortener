from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "https://localhost:8000"
    db_url: str = "sqlite:///./data.db"

    class Config:
        env_file = ".env"


# Cache `get_settings()` function using LRU strategy
# For more: https://realpython.com/lru-cache-python/
@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings: '{settings.env_name}'")
    return settings
