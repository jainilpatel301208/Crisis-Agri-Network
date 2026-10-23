"""Main FastAPI application for Crisis Agriculture & Food Security Network."""

import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.config import settings
from app.models.common import SupportedLanguage
from app.models.request_models import TextDiagnosisRequest
from app.models.response_models import DualTargetDiagnosisResponse, WeatherContext
from app.services.gemini_service import GeminiService
from app.services.language_service import LanguageService
from app.services.weather_service import WeatherService

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multimodal AI network connecting rural farmers to rapid crisis advisory and government food security dashboards."
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "gemini_api_configured": bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 10)
    }


@app.get("/api/languages", tags=["Localization"])
async def list_supported_languages():
    """Return all 15 supported official Indic languages plus English."""
    return LanguageService.get_supported_languages()


@app.get("/api/weather/context", response_model=WeatherContext, tags=["Weather Context"])
async def get_weather_context(
    latitude: float = Query(28.6139, description="Farm latitude"),
    longitude: float = Query(77.2090, description="Farm longitude"),
    preset: Optional[str] = Query(None, description="Optional weather simulation preset")
):
    """Retrieve localized agricultural microclimate weather context."""
    return WeatherService.get_weather_context(latitude, longitude, preset)


@app.post("/api/diagnose/image", response_model=DualTargetDiagnosisResponse, tags=["Diagnosis"])
async def diagnose_crop_image(
    file: UploadFile = File(..., description="Crop leaf/plant image captured by farmer"),
    target_language: str = Form("Hindi", description="Target Indic language for farmer advisory"),
    unstructured_text: Optional[str] = Form(None, description="Transcribed audio or farmer notes"),
    latitude: float = Form(28.6139, description="Field latitude"),
    longitude: float = Form(77.2090, description="Field longitude"),
):
    """
    Multimodal diagnosis accepting image upload, regional language parameter, and audio transcripts.
    Returns both accessible farmer action card and government JSON payload.
    """
    # Validate MIME type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image.")

    image_bytes = await file.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty image file received.")

    response = await GeminiService.analyze_crop(
        image_bytes=image_bytes,
        image_mime_type=file.content_type,
        unstructured_text=unstructured_text or "Diagnose crop leaf condition from image.",
        target_language=target_language,
        latitude=latitude,
        longitude=longitude
    )
    return response


@app.post("/api/diagnose/text", response_model=DualTargetDiagnosisResponse, tags=["Diagnosis"])
async def diagnose_crop_text(payload: TextDiagnosisRequest):
    """
    Diagnose crop issue from unstructured farmer text or voice-to-text transcript.
    """
    response = await GeminiService.analyze_crop(
        image_bytes=None,
        unstructured_text=payload.unstructured_text,
        target_language=payload.target_language.value if hasattr(payload.target_language, 'value') else str(payload.target_language),
        latitude=payload.latitude or 28.6139,
        longitude=payload.longitude or 77.2090
    )
    return response


@app.post("/api/diagnose/sample", response_model=DualTargetDiagnosisResponse, tags=["Diagnosis"])
async def diagnose_sample(
    sample_id: str = Form("wheat_rust", description="Sample scenario: 'wheat_rust', 'rice_blast', 'potato_blight', or 'healthy'"),
    target_language: str = Form("Hindi", description="Target Indic language")
):
    """
    Pre-configured diagnostic scenario for rapid demonstration, testing, and zero-latency evaluation.
    """
    descriptions = {
        "wheat_rust": "Wheat field leaves show bright yellow-orange powder pustules in stripes. Plants are drying out.",
        "rice_blast": "Rice paddy crop has diamond-shaped brown lesions with gray centers on leaf blades and rotten collar.",
        "potato_blight": "Potato foliage shows water-soaked dark lesions with white fungal fuzz underneath in damp weather.",
        "pest_aphid": "Leaves are curling with small green aphids clustering under stems and sticky honeydew.",
        "healthy": "Lush green wheat leaves with vigorous growth and no visible fungal or pest damage."
    }
    sample_text = descriptions.get(sample_id, descriptions["wheat_rust"])

    response = await GeminiService.analyze_crop(
        image_bytes=None,
        unstructured_text=sample_text,
        target_language=target_language,
        latitude=28.6139,
        longitude=77.2090
    )
    return response


# Mount static directory for 3D Three.js frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", tags=["Frontend"])
async def serve_index():
    """Serve the 3D accessible web application."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Crisis Agriculture & Food Security Network API is running. Build frontend static files."}
