"""Common enums and types for Crisis Agriculture Network."""

from enum import Enum


class SeverityLevel(str, Enum):
    """Categorized crop threat severity level."""
    SAFE = "SAFE"
    WARNING = "WARNING"
    DANGER = "DANGER"
    CRITICAL = "CRITICAL"


class PathogenCategory(str, Enum):
    """Pathogen biological taxonomy category."""
    FUNGAL = "FUNGAL"
    BACTERIAL = "BACTERIAL"
    VIRAL = "VIRAL"
    PEST_INSECT = "PEST_INSECT"
    NUTRIENT_DEFICIENCY = "NUTRIENT_DEFICIENCY"
    HEALTHY = "HEALTHY"


class SupportedLanguage(str, Enum):
    """Supported 15 official Indic languages plus English for government views."""
    ASSAMESE = "Assamese"
    BENGALI = "Bengali"
    GUJARATI = "Gujarati"
    KANNADA = "Kannada"
    KASHMIRI = "Kashmiri"
    KONKANI = "Konkani"
    MALAYALAM = "Malayalam"
    MARATHI = "Marathi"
    NEPALI = "Nepali"
    ODIA = "Odia"
    PUNJABI = "Punjabi"
    SANSKRIT = "Sanskrit"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    URDU = "Urdu"
    ENGLISH = "English"
