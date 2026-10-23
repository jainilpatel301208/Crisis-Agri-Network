"""Pytest test configuration and fixtures for Crisis Agriculture Network."""

import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.models.response_models import WeatherContext


@pytest.fixture
def client(monkeypatch):
    """Synchronous test client fixture for FastAPI endpoints."""
    from app.config import settings
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_weather():
    """Mocked microclimate agricultural weather context."""
    return WeatherContext(
        temperature_c=22.5,
        humidity_pct=88.0,
        precipitation_probability_pct=75.0,
        wind_speed_kmh=12.0,
        microclimate_blight_risk="CRITICAL: High humidity elevates fungal spore proliferation.",
        spray_advisory="SPRAYING RESTRICTED: Rain expected within 4 hours.",
        location_name="Agro-Zone Indo-Gangetic Plains"
    )


@pytest.fixture
def dummy_crop_image():
    """Generate in-memory minimalist valid PNG image bytes for testing file uploads."""
    # 1x1 green pixel PNG
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x98\x05\x00'
        b'\x00\x0e\x00\x05\xe7\x02\x15\xbe\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    return io.BytesIO(png_bytes)
