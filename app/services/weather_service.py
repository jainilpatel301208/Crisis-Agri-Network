"""Weather contextualization service for agricultural disease risk modeling."""

import random
from typing import Optional
from app.models.response_models import WeatherContext


class WeatherService:
    """Provides real-time contextual microclimate data for crop pathology evaluation."""

    @staticmethod
    def get_weather_context(
        latitude: Optional[float] = 28.6139,
        longitude: Optional[float] = 77.2090,
        preset: Optional[str] = None
    ) -> WeatherContext:
        """
        Generate contextual microclimate data for crop pathogen analysis.
        Supports presets like 'humid_fungal_risk', 'dry_pest_risk', or geo-derived variation.
        """
        if preset == "humid_fungal_risk":
            temp = 21.5
            humidity = 89.0
            precip = 72.0
            wind = 12.0
            blight_risk = "CRITICAL: Relative humidity >85% and cool temperatures accelerate stripe rust / blight sporulation."
            spray_adv = "SPRAYING RESTRICTED: Rain expected within 4 hours. Chemical runoff risk into soil is severe."
        elif preset == "dry_pest_risk":
            temp = 34.0
            humidity = 38.0
            precip = 5.0
            wind = 18.5
            blight_risk = "LOW FUNGAL / HIGH PEST: Hot, arid conditions suppress fungi but favor aphid and borer multiplication."
            spray_adv = "SPRAYING PERMITTED: Early morning or late evening application only to avoid foliar scorch."
        else:
            # Deterministic variation based on coordinates
            base_seed = int((latitude or 28.0) * 100 + (longitude or 77.0) * 100)
            rng = random.Random(base_seed)
            temp = round(rng.uniform(19.0, 29.0), 1)
            humidity = round(rng.uniform(65.0, 92.0), 1)
            precip = round(rng.uniform(20.0, 80.0), 1)
            wind = round(rng.uniform(6.0, 22.0), 1)

            if humidity > 80:
                blight_risk = "HIGH: Extended humidity elevates fungal spore proliferation and leaf blight."
            elif humidity > 60:
                blight_risk = "MODERATE: Standard monitoring recommended. Inspect undersides of leaves."
            else:
                blight_risk = "LOW: Dry ambient conditions reduce fungal transmission."

            if precip > 60:
                spray_adv = "HOLD APPLICATION: Rain likely. Wait for clear skies before applying foliar remedies."
            elif wind > 18:
                spray_adv = "DRIFT HAZARD: Wind speed > 18 km/h. Avoid aerial or high-pressure spray."
            else:
                spray_adv = "FAVORABLE: Calm atmospheric conditions suitable for targeted bio-spray."

        return WeatherContext(
            temperature_c=temp,
            humidity_pct=humidity,
            precipitation_probability_pct=precip,
            wind_speed_kmh=wind,
            microclimate_blight_risk=blight_risk,
            spray_advisory=spray_adv,
            location_name=f"Agro-Zone Lat {latitude:.2f}°N, Lon {longitude:.2f}°E" if latitude and longitude else "Indo-Gangetic Agro-Climatic Belt"
        )
