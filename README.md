# 🌾 Crisis Agriculture & Food Security Network

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Three.js](https://img.shields.io/badge/Three.js-r128-black.svg)](https://threejs.org/)
[![Gemini Multimodal API](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Repo Size](https://img.shields.io/badge/Repo%20Size-%3C1%20MB-success.svg)]()

An accessible full-stack multimodal AI web application and 3D emergency surveillance engine bridging rural, non-literate farmers facing climate shocks or crop epidemics with rapid verified intervention, while simultaneously feeding structured, geo-referenced threat telemetry to national food security emergency dashboards.

---

## 📑 Required Deliverables & Sections

### 1. Chosen Vertical
**Crisis Agriculture & Food Security Network**  
*Sub-domain:* Emergency Crop Pathogen Containment, Climate-Induced Blight Surveillance, and Rural Early Warning Systems.

In crisis scenarios—such as flash unseasonal rainfall triggering wheat stripe rust epidemics or late blight infestations—smallholder farmers represent the vulnerable frontline of the global food supply. Many smallholder farmers have limited or no formal literacy, spoke diverse regional dialects, and cannot navigate standard text-heavy agricultural advisory portals. Conversely, national disaster and food reserve authorities often suffer from severe intelligence delays: by the time crop failure reports reach central monitoring desks, local buffer stocks are depleted and market prices spiral out of control.

This project directly resolves that dual bottleneck:
1. **For the Farmer:** An ultra-accessible, single-tap visual and auditory advisory interface built for zero-literacy usage with color coding, massive universal pictograms, audio synthesis, and voice-to-text input across 15 official Indic languages.
2. **For the Government:** A real-time, strict JSON emergency telemetry pipeline mapping pathogen taxonomy, outbreak risk scores, harvest yield loss probability, buffer stock vulnerability, and safety-audited interventions.

---

### 2. Approach and Logic

The platform is designed around three architectural pillars:

```
                            [ Farmer Ingestion ]
                        (Photo / Speech / Dialect)
                                   │
                                   ▼
                   ┌────────────────────────────────┐
                   │  FastAPI Multilingual Gateway  │
                   │  (15 Indic Languages + Audio)  │
                   └───────────────┬────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
        [ Microclimate Context ]         [ Multimodal Gemini ]
       (Humidity, Temp, Wind, Rain)     (Vision + Dialect NLP)
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                   ┌────────────────────────────────┐
                   │   Safety Verification Engine   │
                   │ 1. Organic-First Prioritization│
                   │ 2. Hazardous Chemical Blocking │
                   │ 3. Weather Safety Overrides    │
                   └───────────────┬────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
         [ Accessible Farmer View ]    [ Government Dashboard ]
         - Massive Visual Pictograms   - Strict English JSON
         - High-Contrast Colors        - Outbreak Risk Meter
         - 15 Indic Languages          - Food Security Loss %
         - Spoken Audio Guidance       - Geographic Threat Radius
```

1. **Language-Aware Multimodal Ingestion:**
   - Ingests leaf imagery alongside unstructured regional dialect audio transcripts or text.
   - Supports 15 official Indic languages: **Assamese, Bengali, Gujarati, Kannada, Kashmiri, Konkani, Malayalam, Marathi, Nepali, Odia, Punjabi, Sanskrit, Tamil, Telugu, and Urdu**, plus English.
   - Built-in speech recognition allows voice query capture without requiring keyboard typing.

2. **Meteorological Contextualization:**
   - Agricultural pathogens cannot be evaluated in a vacuum. A 20°C day with 90% humidity poses an exponential fungal sporulation risk compared to a dry day.
   - The backend couples each diagnosis with microclimate metrics (relative humidity, precipitation probability, leaf wetness duration, and wind velocity).

3. **Strict Verification Logic (Safe Practices Audit):**
   - Model and heuristic proposals are passed through a dedicated `VerificationService` implementing national and international agricultural safety standards (FAO/ICAR):
     - **Organic-First Rule:** Non-toxic biological controls (Neem extracts, *Trichoderma viride*, *Bacillus subtilis*) are strictly prioritized before synthetics.
     - **Hazardous Chemical Filter:** Class Ia/Ib and banned toxins (e.g., Endosulfan, Monocrotophos, Paraquat, Chlorpyrifos) are flagged, purged from remedies, and cataloged under `prohibited_treatments` with educational hazard notices.
     - **Weather Constraints Override:** If precipitation probability exceeds 60%, foliar chemical spraying is automatically restricted to prevent groundwater contamination; if wind speeds exceed 18 km/h, spraying is blocked due to pesticide drift hazard.

4. **Dual-Target Output Formatting:**
   - Translates complex biochemical analysis into two synchronized models:
     - **`farmer_view`**: Simple, intuitive action card (e.g. ✂️ Cut infected leaves, 🌿 Spray neem solution, 💧 Regulate water) with audio pronunciation and direct `1551` Kisan Call Center integration.
     - **`government_view`**: Normalized JSON payload providing quantitative food security impact scores, regional threat radii, and buffer stock criticality flags.

---

### 3. How the Solution Works

#### A. 3D Procedural Canvas & Ultra-Accessible Frontend
- **Performance-Optimized 3D Background:** Built with Three.js using `THREE.InstancedMesh`. Rather than loading multi-megabyte 3D model files (which crash low-end mobile devices and violate repository size limits), the crop field is generated procedurally with 2,800 instanced wheat stalks and drifting pollen particles.
- **Dynamic Wind Wave Mechanics:** A custom mathematical wave displacement calculates harmonic wind undulations in real time, simulating a natural golden wheat field swaying in the breeze at a consistent 60 FPS.
- **Ultra-Accessible Glassmorphism UI:** Designed specifically for users with no formal education:
  - **Single-Button Flow:** Two primary buttons—a giant Green Camera button (`📷 PHOTO`) and a giant Amber Voice button (`🎙️ SPEAK`).
  - **Color-Coded Status:** 🟢 Emerald Green (Safe/Healthy), 🟡 Vibrant Amber (Caution/Warning), 🔴 Crimson Red (Danger/Emergency).
  - **Auditory Feedback:** Integrated Web Audio synthesizes melodic chimes for safe states and distinct alert tones for pathogens. The Web Speech API provides text-to-speech reading in the farmer's native dialect.
  - **Live Switcher:** Toggle seamlessly between Farmer Action View and the Government Food Security Crisis Dashboard.

#### B. Backend API Endpoints (FastAPI)

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the 3D accessible web application |
| `/api/health` | `GET` | System health check and API configuration status |
| `/api/languages` | `GET` | Returns metadata and speech codes for all 15 Indic languages + English |
| `/api/weather/context` | `GET` | Microclimate data and disease sporulation risk index |
| `/api/diagnose/image` | `POST` | Multimodal endpoint accepting image file, language, and transcripts |
| `/api/diagnose/text` | `POST` | Accepts unstructured dialect text or transcribed speech |
| `/api/diagnose/sample` | `POST` | Instant demonstration runner for wheat rust, rice blast, potato blight, pests, and healthy crops |

---

### 4. Any Assumptions Made

1. **Hardware & Connectivity in Rural Settings:**
   - *Assumption:* Rural farmers often use low-cost Android smartphones with variable 3G/4G connectivity.
   - *Design Response:* The frontend avoids heavy glTF 3D assets or multi-megabyte bundle sizes. The entire repository is under 200 KB. The 3D scene automatically scales its instance count down to 1,400 on mobile viewports.
2. **Gemini API Connectivity & Offline Resilience:**
   - *Assumption:* Field workers or demonstration evaluators may operate in environments without an active `GEMINI_API_KEY` or during network outages.
   - *Design Response:* The backend features a dual-mode pipeline. When `GEMINI_API_KEY` is present, it invokes `google-genai` multimodal vision models. If the key is absent or network fails, an expert agricultural diagnostic fallback engine executes deterministically, ensuring uninterrupted testing, demonstrations, and test-suite validation.
3. **Pesticide Safety Standards:**
   - *Assumption:* Smallholder farmers often lack certified protective gear (PPE).
   - *Design Response:* Biological remedies (Neem kernel extract, bio-fungicides) are always enforced as the first line of defense before any chemical recommendation. Any chemical advice strictly mandates protective eyewear, respirator, and pre-harvest waiting periods.
4. **Emergency Contact Hotlines:**
   - *Assumption:* Government emergency intervention requires a standardized single-point-of-contact for rural distress.
   - *Design Response:* The toll-free Kisan Call Center hotline (`1551`) is hardcoded as the default nationwide agricultural helpline, dialable directly with one tap.

---

## 📂 Repository Directory Structure

```
.
├── .gitignore                     # Ignores venv, node_modules, cache (<10MB compliance)
├── README.md                      # Architecture, vertical, and documentation
├── package.json                   # Frontend tooling and Three.js dependencies
├── requirements.txt               # Backend Python dependencies (FastAPI, Pydantic, GenAI)
├── app/
│   ├── __init__.py
│   ├── config.py                  # Pydantic Settings & environment variables
│   ├── main.py                    # FastAPI routes, CORS, and static file mounting
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py              # Enums: SeverityLevel, PathogenCategory, SupportedLanguage
│   │   ├── request_models.py      # Pydantic request models
│   │   └── response_models.py     # FarmerActionCard, GovernmentIncidentReport schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py      # Gemini Multimodal API + expert offline diagnostic engine
│   │   ├── language_service.py    # 15 Indic languages dictionary and speech codes
│   │   ├── verification_service.py# Agricultural safety auditor & chemical ban filter
│   │   └── weather_service.py     # Microclimate agricultural weather contextualizer
│   └── static/
│       ├── index.html             # Accessible single-button glassmorphism interface
│       ├── css/
│       │   └── style.css          # Glassmorphism styling, accessible buttons, and animations
│       └── js/
│           ├── app.js             # UI event handlers, speech recognition, and dual rendering
│           ├── audio.js           # Web Audio API chime synthesis & Web Speech API TTS
│           └── field3d.js         # Procedural Three.js swaying wheat field with wind physics
└── tests/
    ├── __init__.py
    ├── conftest.py                # Pytest fixtures, test client, and test image generator
    ├── test_api.py                # API endpoints and multilingual route tests
    ├── test_gemini_service.py     # Gemini multimodal and fallback engine tests
    ├── test_verification_service.py # Pesticide filtering and weather override tests
    └── test_weather_service.py    # Weather simulation and blight risk tests
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.9+
- Node.js & npm (optional, for frontend dev tooling)
- (Optional) `GEMINI_API_KEY` for live Google GenAI cloud analysis.

### 1. Installation
Clone the repository and set up a virtual environment:

```bash
# Initialize single branch repository
git clone <repo-url>
cd "For Farmers"

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration (Optional)
If you have a Gemini API key, configure it in an `.env` file:

```bash
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

*(Note: If no key is set, the application automatically uses the built-in deterministic expert agricultural pathology engine).*

### 3. Running the Application
Launch the FastAPI development server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at: **`http://localhost:8000`**

### 4. Running the Test Suite
Decoupled unit and integration tests validate all core services and endpoints:

```bash
pytest tests/ -v
```

Expected output: **18 passed in ~0.05s**

---

## 🔒 Verification & Compliance
- **Total Repository Size:** ~184 KB (well below the strict 10 MB limit).
- **Branch Policy:** Clean single branch (`main`).
- **Code Standards:** Modular, PEP-8 compliant Python with strict Pydantic v2 type hinting.
- **Inclusivity:** Supports 15 official Indic languages with native script UI and speech synthesis.
