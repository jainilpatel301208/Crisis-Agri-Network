"""Application configuration using Pydantic Settings."""

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for Crisis Agriculture & Food Security Network."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "Crisis Agriculture & Food Security Network"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-3.8-flash"

    # CORS Allowed Origins
    CORS_ORIGINS: List[str] = ["*"]

    # National / Regional Hotline for Farmers (e.g., Kisan Call Center India)
    FARMER_EMERGENCY_HOTLINE: str = "1551"


settings = Settings()
