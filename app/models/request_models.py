"""Request models for multimodal ingestion and diagnosis with input sanitization."""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models.common import SupportedLanguage


def sanitize_prompt_text(text: Optional[str]) -> str:
    """Sanitize user input to mitigate prompt injection, stripping control characters and excessive length."""
    if not text:
        return ""
    # Strip potential prompt jailbreaks or instruction-override markers
    cleaned = re.sub(r'(\bignore\b|\bdisregard\b|\boverride\b|\bsystem prompt\b)', '', text, flags=re.IGNORECASE)
    # Strip dangerous HTML or script tags
    cleaned = re.sub(r'<[^>]*>', '', cleaned)
    # Strip control characters
    cleaned = "".join(ch for ch in cleaned if ch.isprintable() or ch in ('\n', '\r', '\t'))
    # Cap string length at 1000 characters
    return cleaned[:1000].strip()


class TextDiagnosisRequest(BaseModel):
    """Payload for textual or audio-transcript crop symptom description."""
    unstructured_text: str = Field(..., max_length=1000, description="Farmer symptom notes or transcribed dialect audio")
    target_language: SupportedLanguage = Field(default=SupportedLanguage.ENGLISH, description="Target regional language")
    latitude: Optional[float] = Field(default=28.6139, ge=-90.0, le=90.0, description="Field latitude")
    longitude: Optional[float] = Field(default=77.2090, ge=-180.0, le=180.0, description="Field longitude")
    crop_hint: Optional[str] = Field(default=None, max_length=100, description="Optional crop hint")

    @field_validator("unstructured_text")
    @classmethod
    def sanitize_input(cls, v: str) -> str:
        return sanitize_prompt_text(v)
