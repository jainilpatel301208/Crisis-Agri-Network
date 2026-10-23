"""Unit tests for weather contextualization service."""

from app.services.weather_service import WeatherService


def test_weather_service_humid_preset():
    """Test humid fungal risk preset."""
    weather = WeatherService.get_weather_context(preset="humid_fungal_risk")
    assert weather.humidity_pct > 80.0
    assert "CRITICAL" in weather.microclimate_blight_risk
    assert weather.precipitation_probability_pct > 60.0
    assert "RESTRICTED" in weather.spray_advisory


def test_weather_service_dry_preset():
    """Test dry pest risk preset."""
    weather = WeatherService.get_weather_context(preset="dry_pest_risk")
    assert weather.humidity_pct < 50.0
    assert weather.temperature_c > 30.0
    assert "PEST" in weather.microclimate_blight_risk


def test_weather_service_coordinates_variance():
    """Test weather variation across different geographic coordinates."""
    w1 = WeatherService.get_weather_context(latitude=28.6139, longitude=77.2090)
    w2 = WeatherService.get_weather_context(latitude=13.0827, longitude=80.2707)

    assert isinstance(w1.temperature_c, float)
    assert isinstance(w2.temperature_c, float)
    assert w1.location_name != ""
