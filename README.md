# Crisis Agriculture & Food Security Network

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Gemini Multimodal API](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Repo Size](https://img.shields.io/badge/Repo%20Size-%3C500%20KB-success.svg)]()

An enterprise-grade multimodal artificial intelligence platform engineered for national food security crisis management, rapid crop pathogen containment, and regional disaster surveillance. The system bridges rural smallholder farmers with immediate, localized, safe action protocols while simultaneously generating real-time, structured telemetry for government disaster command dashboards.

---

## 1. Chosen vertical: (Societal Benefit - Crisis Agriculture)

In crisis scenarios—such as flash unseasonal precipitation triggering wheat stripe rust epidemics or rapid potato late blight sporulation—smallholder farmers represent the vulnerable frontline of the global food supply. Many smallholder farmers have limited or no formal literacy, speak diverse regional dialects, and cannot navigate standard text-heavy agricultural advisory portals. Conversely, national disaster and food reserve authorities often suffer from severe intelligence delays: by the time crop failure reports reach central monitoring desks, local buffer stocks are depleted and market prices spiral out of control.

This project delivers societal impact by resolving that dual bottleneck:
1. **For the Farmer:** An ultra-accessible, single-tap visual and auditory advisory interface built for zero-literacy usage with color-coded alerts, clear action steps, audio synthesis, and voice-to-text input across 15 official Indian languages.
2. **For the Government:** A real-time, strict JSON emergency telemetry pipeline mapping pathogen taxonomy, outbreak risk scores, harvest yield loss probability, buffer stock vulnerability, and safety-audited interventions.

---

## 2. Approach and logic: (How the system acts as an AI bridge)

The platform functions as an intelligent bidirectional translation layer connecting messy, low-bandwidth field observations with high-rigor agronomic intelligence:

```
                            [ Field Ingestion ]
                 (Crop Leaf Image / Dialect Voice / Notes)
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  FastAPI Multilingual Gateway │
                    │ (Prompt Injection Sanitizer)  │
                    └───────────────┬───────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
        [ Microclimate Context ]         [ Multimodal Gemini ]
       (Humidity, Temp, Wind, Rain)     (Vision + Dialect NLP)
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   Safety Verification Engine  │
                    │ 1. Organic-First Priority     │
                    │ 2. Hazardous Chemical Filter  │
                    │ 3. Weather Safety Overrides   │
                    └───────────────┬───────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
          [ Farmer Action Plan ]        [ Government Telemetry ]
          - Legible Localized Text      - Strict English JSON
          - 15 Indian Languages         - Outbreak Risk Metric
          - Audio Guidance (TTS)        - Yield Loss & Buffer Impact
          - Emergency Helpline          - Resource Routing Logistics
```

- **Input Sanitization & Security:** All textual inputs and audio transcripts are processed through `sanitize_prompt_text()` to strip prompt injection vectors, instruction-override attempts, and malicious control characters before reaching the model.
- **Multilingual Routing:** Seamlessly maps input to 15 Indian languages: **Assamese, Bengali, Gujarati, Kannada, Kashmiri, Konkani, Malayalam, Marathi, Nepali, Odia, Punjabi, Sanskrit, Tamil, Telugu, and Urdu**, plus English.
- **Microclimate Contextualization:** Correlates leaf pathology with humidity, temperature, precipitation probability, and wind velocity to calculate true biological sporulation risk.
- **Verification Logic:** Strict verification filters enforce non-toxic, organic solutions (Neem extract, *Trichoderma viride*) first, automatically excise hazardous Class Ia/Ib chemicals (Endosulfan, Monocrotophos, Paraquat), and enforce weather-based spraying overrides.

---

## 3. How the solution works: (Step-by-step pipeline explanation)

1. **Specimen Ingestion:**
   - Field workers or farmers upload a crop leaf image via the drag-and-drop gateway or record regional dialect symptom audio via the Web Speech API interface.
2. **Telemetry Formulation:**
   - The FastAPI backend captures the payload, retrieves real-time microclimate metrics for the farm's GPS coordinates, and formats a structured multimodal prompt with system instructions.
3. **Multimodal Analysis via Gemini:**
   - The multimodal model evaluates visual chlorosis/pustule patterns, analyzes textual symptom descriptions, and contextualizes the data against ambient humidity and temperature.
4. **Safety Audit & Verification:**
   - The `VerificationService` cross-references identified pathogens with approved ICAR/FAO agronomic standards:
     - Enforces non-toxic/organic bio-fungicide protocols as the primary line of defense.
     - Detects and quarantines restricted/banned agrochemicals into an explicit warning list.
     - Checks rain probability (>60%) and wind velocity (>18 km/h) to override foliar spray recommendations.
5. **Dual-Target Dispatch:**
   - **Farmer Action Plan:** Renders a clean localized action card with clear steps, audio speech playback, and direct 1-tap connection to the national Kisan Call Center (`1551`).
   - **Enterprise Telemetry Dashboard:** Generates structured quantitative metrics (Outbreak Risk Index %, Yield Loss Risk %, Spread Radius km, Buffer Stock Criticality, Resource Routing Logistics) and raw JSON export with one-click clipboard copying.

---

## 4. Any assumptions made: (e.g., API limits, simulated environmental data)

1. **API Limits & Offline Resilience:**
   - *Assumption:* Field workers or demonstration evaluators may operate in environments without an active `GEMINI_API_KEY` or during network outages.
   - *Design Response:* The backend features a dual-mode pipeline. When `GEMINI_API_KEY` is present, it invokes `google-genai` multimodal vision models. If the key is absent or network fails, an expert agricultural diagnostic fallback engine executes deterministically, ensuring uninterrupted testing, demonstrations, and test-suite validation.
2. **Environmental & Sensor Telemetry:**
   - *Assumption:* Real-time IoT agro-weather stations are not ubiquitously deployed across all rural farm parcels.
   - *Design Response:* The platform utilizes a deterministic microclimate simulation service (`WeatherService`) that derives ambient temperature, relative humidity, precipitation probability, and wind velocity from latitude/longitude coordinates and agro-climatic zones.
3. **Pesticide Safety Standards:**
   - *Assumption:* Smallholder farmers often lack certified protective gear (PPE).
   - *Design Response:* Biological remedies (Neem kernel extract, bio-fungicides) are always enforced as the first line of defense before any chemical recommendation. Any chemical advice strictly mandates protective eyewear, respirator, and pre-harvest waiting periods.
4. **Emergency Contact Hotlines:**
   - *Assumption:* Government emergency intervention requires a standardized single-point-of-contact for rural distress.
   - *Design Response:* The toll-free Kisan Call Center hotline (`1551`) is hardcoded as the default nationwide agricultural helpline, dialable directly with one tap.

---

## 📂 Directory Layout

```
.
├── .gitignore                       # Ensures repository size remains strictly < 10 MB
├── README.md                        # Complete project documentation
├── package.json                     # Frontend scripts & tooling
├── requirements.txt                 # Backend dependencies (FastAPI, Pydantic, GenAI, Pytest)
├── app/
│   ├── __init__.py
│   ├── config.py                    # Environment settings and API keys
│   ├── main.py                      # FastAPI application and route declarations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py                # Enums: SeverityLevel, PathogenCategory, SupportedLanguage
│   │   ├── request_models.py        # Text & voice transcript ingestion models
│   │   └── response_models.py       # FarmerActionPlan & GovernmentTelemetryReport schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py        # Multimodal Gemini integration & expert fallback engine
│   │   ├── language_service.py      # 15 Indian languages registry & localized vocabularies
│   │   ├── verification_service.py  # Pathogen safety audit & banned pesticide filters
│   │   └── weather_service.py       # Microclimate weather contextualization & blight risk
│   └── static/
│       ├── index.html               # Enterprise dashboard interface
│       ├── css/
│       │   └── style.css            # Clean, minimalist SaaS styling (Inter typography)
│       └── js/
│           ├── app.js               # Ingestion logic, speech-to-text, telemetry rendering
│           └── audio.js             # Web Audio API cues & Web Speech API TTS synthesis
└── tests/
    ├── __init__.py
    ├── conftest.py                  # Pytest fixtures, TestClient, mock weather & image bytes
    ├── test_api.py                  # API endpoints and multilingual route tests
    ├── test_gemini_service.py       # Gemini multimodal & expert fallback engine tests
    ├── test_verification_service.py # Organic-first hierarchy & pesticide safety checks
    └── test_weather_service.py      # Weather risk modeling tests
```

---

## 🚀 Quickstart Guide

### 1. Installation
```bash
# Clone the repository
git clone <repo-url>
cd "For Farmers"

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration (Optional)
If you have a Gemini API key:
```bash
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```
*(If no key is configured, the application automatically uses the built-in deterministic expert agricultural pathology engine).*

### 3. Launching the Enterprise Dashboard
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser at: **`http://localhost:8000`**

### 4. Running the Test Suite
```bash
pytest tests/ -v
```
Expected output: **20 passed in ~0.04s**
