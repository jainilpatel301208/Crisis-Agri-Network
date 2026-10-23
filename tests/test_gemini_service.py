"""Unit tests for Gemini Service multimodal analysis and dual-target routing."""

import pytest
from unittest.mock import patch, MagicMock
from app.services.gemini_service import GeminiService
from app.models.common import SeverityLevel, PathogenCategory


@pytest.mark.asyncio
async def test_expert_fallback_wheat_rust():
    """Test expert fallback engine detecting Wheat Yellow Rust."""
    response = await GeminiService.analyze_crop(
        image_bytes=None,
        unstructured_text="The wheat leaves are covered in powdery yellow rust lines.",
        target_language="Punjabi"
    )

    assert response.success is True
    assert "Wheat" in response.government_view.crop_identified
    assert "Rust" in response.government_view.pathogen_common_name
    assert response.government_view.severity_level in [SeverityLevel.CRITICAL, SeverityLevel.DANGER]
    assert response.farmer_view.primary_action_icon in ["✂️", "🌿"]
    assert response.farmer_view.audio_cue in ["alert", "warning"]


@pytest.mark.asyncio
async def test_expert_fallback_potato_blight():
    """Test expert fallback engine detecting Potato Late Blight."""
    response = await GeminiService.analyze_crop(
        image_bytes=None,
        unstructured_text="Potato plant leaves turning black with water-soaked rot and white mold.",
        target_language="Bengali"
    )

    assert response.success is True
    assert "Potato" in response.government_view.crop_identified
    assert "Late Blight" in response.government_view.pathogen_common_name
    assert response.government_view.food_security_impact.yield_loss_risk_pct >= 50.0


@pytest.mark.asyncio
async def test_mocked_gemini_api_call():
    """Test GeminiService with mocked google.genai Client."""
    mock_json_response = {
        "crop_identified": "Cotton (Gossypium)",
        "pathogen_scientific_name": "Helicoverpa armigera",
        "pathogen_common_name": "Cotton Bollworm",
        "pathogen_category": "PEST_INSECT",
        "severity_level": "DANGER",
        "outbreak_risk_score": 0.82,
        "food_security_impact": {
            "yield_loss_risk_pct": 40.0,
            "regional_threat_radius_km": 30.0,
            "buffer_stock_criticality": "VULNERABLE",
            "estimated_hectares_at_risk": 2500.0
        },
        "proposed_remedies": ["Install pheromone traps", "Spray bio-pesticide"],
        "farmer_view": {
            "status_headline": "सावधान! बोंड अळीचा प्रादुर्भाव",
            "primary_action_icon": "🐛",
            "simple_steps": ["1. फेरोमोन ट्रॅप लावा", "2. कडुनिंब तेल फवारा"],
            "audio_summary": "बोंड अळीचा प्रादुर्भाव झाला आहे. लगेच उपाय करा.",
            "audio_cue": "alert",
            "do_not_list": ["विषारी मोनोक्रोटोफॉस वापरू नका"]
        }
    }

    with patch("app.services.gemini_service.settings") as mock_settings:
        mock_settings.GEMINI_API_KEY = "test-api-key-12345"
        mock_settings.GEMINI_MODEL = "gemini-2.5-flash"
        mock_settings.FARMER_EMERGENCY_HOTLINE = "1551"

        with patch.object(GeminiService, "_call_gemini_api", return_value=mock_json_response):
            response = await GeminiService.analyze_crop(
                image_bytes=b"fake-bytes",
                unstructured_text="Cotton bolls damaged by worm holes",
                target_language="Marathi"
            )

            assert response.success is True
            assert response.government_view.crop_identified == "Cotton (Gossypium)"
            assert response.government_view.pathogen_category == PathogenCategory.PEST_INSECT
            assert response.farmer_view.primary_action_icon == "🐛"
