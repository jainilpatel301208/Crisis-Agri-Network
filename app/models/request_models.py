"""Request models for multimodal ingestion and diagnosis."""

from typing import Optional
from pydantic import BaseModel, Field
from app.models.common import SupportedLanguage


class TextDiagnosisRequest(BaseModel):
    """Payload for textual or audio-transcript crop issue description."""
    unstructured_text: str = Field(..., description="Messy farmer text or transcribed regional dialect audio")
    target_language: SupportedLanguage = Field(default=SupportedLanguage.HINDI if hasattr(SupportedLanguage, 'HINDI') else SupportedLanguage.ENGLISH)
    latitude: Optional[float] = Field(default=28.6139, description="Field latitude")
    longitude: Optional[float] = Field(default=77.2090, description="Field longitude")
    crop_hint: Optional[str] = Field(default=None, description="Optional crop hint (e.g., wheat, rice, potato)")
