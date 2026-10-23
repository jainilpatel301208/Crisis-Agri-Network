"""Unit tests for agricultural safety verification logic."""

from app.services.verification_service import VerificationService
from app.models.response_models import WeatherContext


def test_verification_organic_first_hierarchy(mock_weather):
    """Verify organic treatments always take priority."""
    verified, prohibited, audit_status = VerificationService.verify_remedies(
        pathogen_name="Puccinia striiformis (Yellow Rust)",
        pathogen_category="FUNGAL",
        proposed_remedies=["Spray fungicide chemical", "Use neem oil"],
        weather=mock_weather
    )

    # Check organic is present
    organic_found = any("Organic" in rem for rem in verified)
    assert organic_found is True


def test_verification_banned_chemical_elimination(mock_weather):
    """Verify hazardous banned chemicals (e.g. Endosulfan, Monocrotophos) are filtered."""
    unsafe_proposals = [
        "Spray Endosulfan at 2ml/L",
        "Apply Monocrotophos immediately",
        "Use cold neem extract"
    ]

    verified, prohibited, audit_status = VerificationService.verify_remedies(
        pathogen_name="Rice Blast",
        pathogen_category="FUNGAL",
        proposed_remedies=unsafe_proposals,
        weather=mock_weather
    )

    # Check that Endosulfan and Monocrotophos are moved to prohibited
    prohibited_text = " ".join(prohibited).lower()
    assert "endosulfan" in prohibited_text
    assert "monocrotophos" in prohibited_text

    # Verified list must not have Endosulfan as an approved item
    for rem in verified:
        assert "endosulfan at 2ml/l" not in rem.lower()


def test_verification_weather_rain_restriction():
    """Verify rainfall above 60% triggers a spray restriction override."""
    rainy_weather = WeatherContext(
        temperature_c=24.0,
        humidity_pct=92.0,
        precipitation_probability_pct=85.0,
        wind_speed_kmh=10.0,
        microclimate_blight_risk="HIGH",
        spray_advisory="DO NOT SPRAY: Torrential rain forecast."
    )

    verified, prohibited, audit_status = VerificationService.verify_remedies(
        pathogen_name="Late Blight",
        pathogen_category="FUNGAL",
        proposed_remedies=["Apply copper spray"],
        weather=rainy_weather
    )

    assert audit_status == "VERIFIED_HOLD_DUE_TO_RAIN"
    assert any("Rainfall risk" in rem for rem in verified)


def test_verification_weather_wind_restriction():
    """Verify wind speed above 18 km/h triggers spray drift restriction."""
    windy_weather = WeatherContext(
        temperature_c=28.0,
        humidity_pct=60.0,
        precipitation_probability_pct=10.0,
        wind_speed_kmh=24.5,
        microclimate_blight_risk="LOW",
        spray_advisory="HIGH DRIFT"
    )

    verified, prohibited, audit_status = VerificationService.verify_remedies(
        pathogen_name="Wheat Rust",
        pathogen_category="FUNGAL",
        proposed_remedies=["Spray foliar bio-fungicide"],
        weather=windy_weather
    )

    assert audit_status == "VERIFIED_HOLD_DUE_TO_WIND"
    assert any("Wind speed is" in rem for rem in verified)
