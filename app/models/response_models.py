"""Response schemas for farmer action plan and enterprise government telemetry."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.common import SeverityLevel, PathogenCategory


class FarmerActionPlan(BaseModel):
    """Localized, legible action plan strictly for rural farmer comprehension."""
    severity: SeverityLevel
    severity_badge_class: str = Field(default="danger", description="CSS badge class: success, warning, danger, critical")
    status_headline: str = Field(description="Clear localized status headline in target language")
    action_protocol: List[str] = Field(description="Sequential verified steps in target language")
    audio_transcript: str = Field(description="Spoken phonetic summary for audio synthesizer")
    restricted_practices: List[str] = Field(default_factory=list, description="Strictly prohibited toxic practices in target language")
    emergency_extension_contact: str = Field(default="1551", description="National Farmer Emergency Helpline")


class WeatherContext(BaseModel):
    """Contextual microclimate and meteorological telemetry."""
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


class ResourceRouting(BaseModel):
    """Government emergency logistics and field containment dispatch."""
    containment_status: str = Field(description="CONTAINED, ACTIVE_SURVEILLANCE, RAPID_RESPONSE_REQUIRED")
    recommended_bio_fungicide_kg: float = Field(description="Estimated organic containment inventory needed in kg")
    field_officers_dispatched: int = Field(description="Recommended agricultural extension personnel")
    buffer_stock_depot: str = Field(description="Nearest designated Food Corporation / emergency reserve silo")
    priority_level: str = Field(description="LOW, MEDIUM, HIGH, CRITICAL_EMERGENCY")


class DiseaseClassification(BaseModel):
    """Pathology taxonomy and biological classification."""
    crop: str
    common_name: str
    scientific_name: str
    category: PathogenCategory
    pathogen_virulence_index: float = Field(ge=0.0, le=1.0)


class GeoCoordinates(BaseModel):
    """Geographic positioning and agro-climatic zoning."""
    latitude: float
    longitude: float
    agro_climatic_zone: str
    district_ref: Optional[str] = "Zone 4 - Gangetic Agricultural Basin"


class VisualSpecimenAnalysis(BaseModel):
    """Computer vision metrics extracted from uploaded crop specimen imagery."""
    specimen_detected: bool = True
    dominant_pattern: str = Field(description="e.g. Chlorotic Yellow Rust Pustules, Necrotic Blight Lesions, Vigorous Green")
    rust_pustule_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    blight_necrosis_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    healthy_canopy_pct: float = Field(default=100.0, ge=0.0, le=100.0)
    diagnostic_confidence_pct: float = Field(default=92.5, ge=0.0, le=100.0)


class GovernmentTelemetryReport(BaseModel):
    """Strict JSON telemetry schema for enterprise government dashboards and disaster response."""
    report_id: str
    timestamp: str
    severity: SeverityLevel
    disease_classification: DiseaseClassification
    outbreak_risk_score: float = Field(ge=0.0, le=1.0)
    geo_coordinates: GeoCoordinates
    weather_telemetry: WeatherContext
    food_security_impact: FoodSecurityImpact
    resource_routing: ResourceRouting
    verified_safe_remedies: List[str]
    prohibited_treatments: List[str]
    visual_analysis: Optional[VisualSpecimenAnalysis] = None
    safety_audit_status: str = Field(default="VERIFIED_SAFE_ORGANIC_FIRST")


class DualTargetDiagnosisResponse(BaseModel):
    """Enterprise dual-target response separating Farmer Action Plan and Government Telemetry."""
    success: bool = True
    target_language: str
    farmer_view: FarmerActionPlan
    government_view: GovernmentTelemetryReport
