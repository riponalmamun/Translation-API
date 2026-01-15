from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # OpenAI API Configuration
    OPENAI_API_KEY: str
    GPT_MODEL: str = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper
    
    # Application Settings
    APP_NAME: str = "Multilingual Translation API"
    DEBUG: bool = False
    
    # API Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 60
    
    # Audio Settings
    MAX_AUDIO_SIZE_MB: int = 25
    SUPPORTED_AUDIO_FORMATS: list = [".mp3", ".wav", ".m4a", ".ogg"]
    
    # Voice Settings
    DEFAULT_VOICE: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()