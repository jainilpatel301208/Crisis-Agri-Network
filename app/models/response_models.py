"""Response schemas for farmer and government dashboard dual-targets."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.common import SeverityLevel, PathogenCategory


class FarmerActionCard(BaseModel):
    """Ultra-accessible action plan designed for rural farmers with zero formal literacy."""
    severity: SeverityLevel
    severity_color: str = Field(description="Hex color code: Green (#10b981), Amber (#f59e0b), Red (#ef4444)")
    status_headline: str = Field(description="Short 2-4 word headline in native target language")
    primary_action_icon: str = Field(description="Large visual symbol/emoji indicating primary action")
    simple_steps: List[str] = Field(description="Visual, numbered action steps in native target language")
    audio_summary: str = Field(description="Spoken phonetic summary string for Text-to-Speech")
    audio_cue: str = Field(default="alert", description="Sound signature type: 'positive', 'warning', or 'alert'")
    do_not_list: List[str] = Field(default_factory=list, description="Things strictly to avoid in native language")
    emergency_helpline: str = Field(default="1551", description="Farmer crisis toll-free hotline")


class WeatherContext(BaseModel):
    """Contextual microclimate and meteorological data."""
    temperature_c: float
    humidity_pct: float
    precipitation_probability_pct: float
    wind_speed_kmh: float
    microclimate_blight_risk: str
    spray_advisory: str
    location_name: Optional[str] = "Regional Agricultural Zone"


class FoodSecurityImpact(BaseModel):
    """Macro-economic and food security threat evaluation."""
    yield_loss_risk_pct: float = Field(ge=0.0, le=100.0)
    regional_threat_radius_km: float
    buffer_stock_criticality: str = Field(description="NORMAL, WATCH, VULNERABLE, or EMERGENCY_MOBILIZATION")
    estimated_hectares_at_risk: float


class GovernmentIncidentReport(BaseModel):
    """Strict English JSON schema for agricultural emergency & food security dashboards."""
    report_id: str
    timestamp: str
    crop_identified: str
    pathogen_scientific_name: str
    pathogen_common_name: str
    pathogen_category: PathogenCategory
    severity_level: SeverityLevel
    outbreak_risk_score: float = Field(ge=0.0, le=1.0, description="Outbreak index from 0.0 to 1.0")
    verified_safe_remedies: List[str]
    prohibited_treatments: List[str]
    weather_context: WeatherContext
    food_security_impact: FoodSecurityImpact
    geo_location: Dict[str, Any]
    safety_audit_status: str = Field(default="VERIFIED_SAFE")


class DualTargetDiagnosisResponse(BaseModel):
    """Unified dual-target response containing both accessible farmer card and government report."""
    success: bool = True
    target_language: str
    farmer_view: FarmerActionCard
    government_view: GovernmentIncidentReport
