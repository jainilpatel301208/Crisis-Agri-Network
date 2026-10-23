/**
 * Enterprise Application Logic
 * Telemetry Ingestion, Computer Vision Specimen Processing, Gemini Multimodal API Bridge,
 * Operational View Routing, and Multilingual Audio Advisory
 */

document.addEventListener("DOMContentLoaded", () => {
  const audioCtrl = new AudioController();

  // State: Default strictly set to English
  let currentTargetLang = "English";
  let currentSpeechCode = "en-US";
  let selectedImageFile = null;
  let isListeningVoice = false;
  let recognition = null;
  let currentTelemetryData = null;

  // DOM Elements
  const langSelect = document.getElementById("lang-select");
  const stageHeaderTitle = document.getElementById("stage-header-title");
  const geminiStatusLabel = document.getElementById("gemini-status-label");

  // Navigation Items & View Sections
  const navSurveillance = document.getElementById("nav-surveillance");
  const navBuffer = document.getElementById("nav-buffer");
  const navDispatch = document.getElementById("nav-dispatch");
  const navSafety = document.getElementById("nav-safety");

  const viewSurveillance = document.getElementById("view-section-surveillance");
  const viewBuffer = document.getElementById("view-section-buffer");
  const viewDispatch = document.getElementById("view-section-dispatch");
  const viewSafety = document.getElementById("view-section-safety");

  // Ingestion Elements
  const dropzone = document.getElementById("dropzone");
  const imageFileInput = document.getElementById("image-file-input");
  const imagePreviewBox = document.getElementById("image-preview-box");
  const imagePreviewImg = document.getElementById("image-preview-img");
  const btnRemoveImage = document.getElementById("btn-remove-image");

  const btnVoiceToggle = document.getElementById("btn-voice-toggle");
  const voiceStatusText = document.getElementById("voice-status-text");
  const symptomNotes = document.getElementById("symptom-notes");
  const inputLat = document.getElementById("input-lat");
  const inputLon = document.getElementById("input-lon");
  const btnDetectGps = document.getElementById("btn-detect-gps");
  const btnSubmitAudit = document.getElementById("btn-submit-audit");
  const loaderBox = document.getElementById("loader-box");

  // Tabs
  const tabBtnFarmer = document.getElementById("tab-btn-farmer");
  const tabBtnGovt = document.getElementById("tab-btn-govt");
  const tabContentFarmer = document.getElementById("tab-content-farmer");
  const tabContentGovt = document.getElementById("tab-content-govt");

  // Overview Banner Metrics
  const valSeverity = document.getElementById("val-severity");
  const valRiskIndex = document.getElementById("val-risk-index");
  const valYieldLoss = document.getElementById("val-yield-loss");
  const valThreatRadius = document.getElementById("val-threat-radius");

  // Visual Diagnostics Elements
  const valVisionPattern = document.getElementById("val-vision-pattern");
  const valVisionConf = document.getElementById("val-vision-conf");
  const valVisionRust = document.getElementById("val-vision-rust");
  const valVisionBlight = document.getElementById("val-vision-blight");
  const valVisionHealthy = document.getElementById("val-vision-healthy");

  // Farmer Plan Elements
  const farmerHeadlineText = document.getElementById("farmer-headline-text");
  const btnAudioListen = document.getElementById("btn-audio-listen");
  const actionProtocolList = document.getElementById("action-protocol-list");
  const warningAlertBox = document.getElementById("warning-alert-box");
  const warningAlertText = document.getElementById("warning-alert-text");

  // Government Telemetry Elements
  const telCrop = document.getElementById("tel-crop");
  const telPathogenCom = document.getElementById("tel-pathogen-com");
  const telPathogenSci = document.getElementById("tel-pathogen-sci");
  const telCategory = document.getElementById("tel-category");
  const telVirulence = document.getElementById("tel-virulence");

  const telContainment = document.getElementById("tel-containment");
  const telBioFungicide = document.getElementById("tel-bio-fungicide");
  const telOfficers = document.getElementById("tel-officers");
  const telDepot = document.getElementById("tel-depot");
  const telPriority = document.getElementById("tel-priority");

  const telWeatherBlight = document.getElementById("tel-weather-blight");
  const telWeatherSpray = document.getElementById("tel-weather-spray");
  const telInterventionsList = document.getElementById("tel-interventions-list");
  const jsonInspector = document.getElementById("json-inspector");
  const btnCopyJson = document.getElementById("btn-copy-json");

  // API Key Modal Elements
  const btnToggleKeyModal = document.getElementById("btn-toggle-key-modal");
  const modalApiKey = document.getElementById("modal-api-key");
  const inputApiKeyModal = document.getElementById("input-api-key-modal");
  const btnCancelModal = document.getElementById("btn-cancel-modal");
  const btnSaveKeyModal = document.getElementById("btn-save-key-modal");

  // Live UTC Clock in Header
  function updateLiveClock() {
    const clockBadge = document.getElementById("badge-clock");
    if (clockBadge) {
      const now = new Date();
      clockBadge.textContent = now.toISOString().replace("T", " ").substring(0, 19) + " UTC";
    }
  }
  setInterval(updateLiveClock, 1000);
  updateLiveClock();

  // 1. Navigation Switching Between All 4 Operations Sections
  function switchNav(activeNav, activeViewSection, title) {
    [navSurveillance, navBuffer, navDispatch, navSafety].forEach(n => n.classList.remove("active"));
    [viewSurveillance, viewBuffer, viewDispatch, viewSafety].forEach(v => v.style.display = "none");

    activeNav.classList.add("active");
    activeViewSection.style.display = activeViewSection === viewSurveillance ? "grid" : "block";
    stageHeaderTitle.textContent = title;
  }

  navSurveillance.addEventListener("click", () => switchNav(navSurveillance, viewSurveillance, "Emergency Agronomic Surveillance & Telemetry Feed"));
  navBuffer.addEventListener("click", () => switchNav(navBuffer, viewBuffer, "Strategic National Food Reserves Telemetry"));
  navDispatch.addEventListener("click", () => switchNav(navDispatch, viewDispatch, "Emergency Containment Logistics & Field Mobilization"));
  navSafety.addEventListener("click", () => switchNav(navSafety, viewSafety, "Regulatory Standards & Chemical Safety Audit Protocols"));

  // 2. Fetch Languages with English as Explicit Default
  async function initLanguages() {
    try {
      const res = await fetch("/api/languages");
      if (res.ok) {
        const langs = await res.json();
        langSelect.innerHTML = "";
        
        // Ensure English is first option
        const englishObj = langs.find(l => l.key === "English") || { key: "English", name: "English", native_name: "English", speech_code: "en-US" };
        const otherLangs = langs.filter(l => l.key !== "English");

        const optEng = document.createElement("option");
        optEng.value = englishObj.key;
        optEng.dataset.speechCode = englishObj.speech_code;
        optEng.textContent = `${englishObj.name} - ${englishObj.native_name}`;
        optEng.selected = true;
        langSelect.appendChild(optEng);

        otherLangs.forEach(l => {
          const opt = document.createElement("option");
          opt.value = l.key;
          opt.dataset.speechCode = l.speech_code;
          opt.textContent = `${l.name} - ${l.native_name}`;
          langSelect.appendChild(opt);
        });

        currentTargetLang = "English";
        currentSpeechCode = "en-US";
      }
    } catch (err) {
      console.warn("Language fetch error:", err);
    }
  }
  initLanguages();

  langSelect.addEventListener("change", (e) => {
    const selectedOpt = langSelect.options[langSelect.selectedIndex];
    currentTargetLang = e.target.value;
    currentSpeechCode = selectedOpt.dataset.speechCode || "en-US";

    if (currentTelemetryData) {
      runDiagnosisRequest();
    }
  });

  // 3. Tab Switching
  tabBtnFarmer.addEventListener("click", () => {
    tabBtnFarmer.classList.add("active");
    tabBtnGovt.classList.remove("active");
    tabContentFarmer.style.display = "block";
    tabContentGovt.style.display = "none";
  });

  tabBtnGovt.addEventListener("click", () => {
    tabBtnGovt.classList.add("active");
    tabBtnFarmer.classList.remove("active");
    tabContentGovt.style.display = "block";
    tabContentFarmer.style.display = "none";
  });

  // 4. Geolocation Auto-Detection
  btnDetectGps.addEventListener("click", () => {
    if (navigator.geolocation) {
      btnDetectGps.textContent = "📍 Locating...";
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          inputLat.value = pos.coords.latitude.toFixed(4);
          inputLon.value = pos.coords.longitude.toFixed(4);
          btnDetectGps.textContent = "📍 GPS Updated";
          setTimeout(() => { btnDetectGps.textContent = "📍 Auto-Detect GPS"; }, 2000);
        },
        (err) => {
          alert("Location access denied or unavailable. Using regional agricultural coordinates.");
          btnDetectGps.textContent = "📍 Auto-Detect GPS";
        }
      );
    } else {
      alert("Geolocation is not supported by your browser.");
    }
  });

  // 5. Drag and Drop File Ingestion
  dropzone.addEventListener("click", () => imageFileInput.click());

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleSelectedImage(e.dataTransfer.files[0]);
    }
  });

  imageFileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleSelectedImage(e.target.files[0]);
    }
  });

  function handleSelectedImage(file) {
    if (!file.type.startsWith("image/")) {
      alert("Invalid format. Please select an image file (JPEG, PNG, WebP).");
      return;
    }
    selectedImageFile = file;
    const reader = new FileReader();
    reader.onload = (evt) => {
      imagePreviewImg.src = evt.target.result;
      imagePreviewBox.style.display = "block";
      dropzone.style.display = "none";
    };
    reader.readAsDataURL(file);
  }

  btnRemoveImage.addEventListener("click", (e) => {
    e.stopPropagation();
    selectedImageFile = null;
    imageFileInput.value = "";
    imagePreviewBox.style.display = "none";
    dropzone.style.display = "block";
  });

  // 6. Voice Recognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      isListeningVoice = true;
      btnVoiceToggle.classList.add("listening");
      voiceStatusText.textContent = "Listening...";
    };

    recognition.onresult = (evt) => {
      const transcript = evt.results[0][0].transcript;
      symptomNotes.value = (symptomNotes.value ? symptomNotes.value + " " : "") + transcript;
      stopVoice();
    };

    recognition.onerror = () => stopVoice();
    recognition.onend = () => stopVoice();
  }

  btnVoiceToggle.addEventListener("click", () => {
    if (!recognition) {
      alert("Speech recognition is not supported in this browser. Please type symptoms into the observations field.");
      return;
    }
    if (isListeningVoice) {
      recognition.stop();
      stopVoice();
    } else {
      recognition.lang = currentSpeechCode;
      try {
        recognition.start();
      } catch (err) {
        recognition.stop();
      }
    }
  });

  function stopVoice() {
    isListeningVoice = false;
    btnVoiceToggle.classList.remove("listening");
    voiceStatusText.textContent = "Record Voice";
  }

  // 7. Quick Incident Presets
  document.querySelectorAll(".preset-row").forEach(btn => {
    btn.addEventListener("click", () => {
      const sampleId = btn.dataset.sample;
      runPresetIncident(sampleId);
    });
  });

  async function runPresetIncident(sampleId) {
    setLoading(true);
    const formData = new FormData();
    formData.append("sample_id", sampleId);
    formData.append("target_language", currentTargetLang);

    try {
      const res = await fetch("/api/diagnose/sample", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      renderTelemetry(data);
    } catch (err) {
      console.error("Diagnosis error:", err);
    } finally {
      setLoading(false);
    }
  }

  // 8. Execute Multimodal Pathology Audit
  btnSubmitAudit.addEventListener("click", () => runDiagnosisRequest());

  async function runDiagnosisRequest() {
    setLoading(true);

    try {
      let res;
      if (selectedImageFile) {
        const formData = new FormData();
        formData.append("file", selectedImageFile);
        formData.append("target_language", currentTargetLang);
        formData.append("unstructured_text", symptomNotes.value || "Analyze crop specimen photo for leaf pathology.");
        formData.append("latitude", inputLat.value || "28.6139");
        formData.append("longitude", inputLon.value || "77.2090");

        res = await fetch("/api/diagnose/image", {
          method: "POST",
          body: formData
        });
      } else {
        const payload = {
          unstructured_text: symptomNotes.value || "Field crop foliage showing discoloration and lesions.",
          target_language: currentTargetLang,
          latitude: parseFloat(inputLat.value) || 28.6139,
          longitude: parseFloat(inputLon.value) || 77.2090
        };

        res = await fetch("/api/diagnose/text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
      }

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();
      renderTelemetry(data);
    } catch (err) {
      console.error("Submission error:", err);
      // Fallback
      runPresetIncident("wheat_rust");
    } finally {
      setLoading(false);
    }
  }

  // 9. Render Telemetry & Specimen Visual Diagnostics
  function renderTelemetry(data) {
    currentTelemetryData = data;
    const fView = data.farmer_view;
    const gView = data.government_view;

    // Overview Banner
    valSeverity.textContent = gView.severity;
    valSeverity.className = `metric-value ${fView.severity_badge_class}`;

    valRiskIndex.textContent = `${Math.round(gView.outbreak_risk_score * 100)}%`;
    valYieldLoss.textContent = `${Math.round(gView.food_security_impact.yield_loss_risk_pct)}%`;
    valThreatRadius.textContent = `${gView.food_security_impact.regional_threat_radius_km} km`;

    // Visual Specimen Diagnostics
    if (gView.visual_analysis) {
      valVisionPattern.textContent = gView.visual_analysis.dominant_pattern;
      valVisionConf.textContent = `Optical Confidence: ${Math.round(gView.visual_analysis.diagnostic_confidence_pct)}%`;
      valVisionRust.textContent = `${gView.visual_analysis.rust_pustule_pct.toFixed(1)}%`;
      valVisionBlight.textContent = `${gView.visual_analysis.blight_necrosis_pct.toFixed(1)}%`;
      valVisionHealthy.textContent = `${gView.visual_analysis.healthy_canopy_pct.toFixed(1)}%`;
    }

    // Tab 1: Farmer Action Plan
    farmerHeadlineText.textContent = fView.status_headline;

    actionProtocolList.innerHTML = "";
    (fView.action_protocol || []).forEach((step, idx) => {
      const item = document.createElement("div");
      item.className = "protocol-item";
      item.innerHTML = `
        <span class="protocol-num">${idx + 1}</span>
        <span>${step}</span>
      `;
      actionProtocolList.appendChild(item);
    });

    if (fView.restricted_practices && fView.restricted_practices.length > 0) {
      warningAlertBox.style.display = "flex";
      warningAlertText.textContent = fView.restricted_practices[0];
    } else {
      warningAlertBox.style.display = "none";
    }

    // Audio Playback
    btnAudioListen.onclick = () => {
      btnAudioListen.classList.add("playing");
      audioCtrl.speakText(fView.audio_transcript, currentSpeechCode, () => {
        btnAudioListen.classList.remove("playing");
      });
    };

    // Tab 2: Government Telemetry
    const dClass = gView.disease_classification;
    telCrop.textContent = dClass.crop;
    telPathogenCom.textContent = dClass.common_name;
    telPathogenSci.textContent = dClass.scientific_name;
    telCategory.textContent = dClass.category;
    telVirulence.textContent = dClass.pathogen_virulence_index.toFixed(2);

    const rRoute = gView.resource_routing;
    telContainment.textContent = rRoute.containment_status;
    telBioFungicide.textContent = `${rRoute.recommended_bio_fungicide_kg} kg`;
    telOfficers.textContent = `${rRoute.field_officers_dispatched} Specialists`;
    telDepot.textContent = rRoute.buffer_stock_depot;
    telPriority.textContent = rRoute.priority_level;

    telWeatherBlight.textContent = gView.weather_telemetry.microclimate_blight_risk;
    telWeatherSpray.textContent = gView.weather_telemetry.spray_advisory;

    // Safety Audited Interventions
    telInterventionsList.innerHTML = "";
    gView.verified_safe_remedies.forEach(rem => {
      const li = document.createElement("li");
      li.style.padding = "0.35rem 0";
      li.style.borderBottom = "1px solid var(--border-light)";
      li.textContent = rem;
      telInterventionsList.appendChild(li);
    });

    // Prohibited Chemicals
    if (gView.prohibited_treatments && gView.prohibited_treatments.length > 0) {
      const pHeader = document.createElement("li");
      pHeader.style.paddingTop = "0.5rem";
      pHeader.style.color = "#b91c1c";
      pHeader.style.fontWeight = "700";
      pHeader.textContent = "Prohibited / Banned Agrochemicals:";
      telInterventionsList.appendChild(pHeader);

      gView.prohibited_treatments.forEach(prohib => {
        const li = document.createElement("li");
        li.style.color = "#dc2626";
        li.style.padding = "0.2rem 0";
        li.textContent = `[Blocked] ${prohib}`;
        telInterventionsList.appendChild(li);
      });
    }

    // JSON Inspector
    jsonInspector.textContent = JSON.stringify(gView, null, 2);
  }

  // Copy JSON Payload
  btnCopyJson.addEventListener("click", () => {
    if (currentTelemetryData) {
      navigator.clipboard.writeText(JSON.stringify(currentTelemetryData.government_view, null, 2));
      btnCopyJson.textContent = "Copied!";
      setTimeout(() => { btnCopyJson.textContent = "Copy JSON"; }, 2000);
    }
  });

  // 10. API Key Modal Handlers
  btnToggleKeyModal.addEventListener("click", () => {
    modalApiKey.style.display = "flex";
  });

  btnCancelModal.addEventListener("click", () => {
    modalApiKey.style.display = "none";
  });

  btnSaveKeyModal.addEventListener("click", async () => {
    const keyVal = inputApiKeyModal.value.trim();
    try {
      const res = await fetch("/api/settings/api-key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: keyVal })
      });
      const data = await res.json();
      modalApiKey.style.display = "none";
      if (data.configured) {
        geminiStatusLabel.textContent = "Gemini Live API: Connected";
        alert("Google Gemini API key registered successfully!");
      } else {
        geminiStatusLabel.textContent = "Multimodal AI Engine: Active";
      }
    } catch (err) {
      alert("Failed to update API key: " + err);
    }
  });

  function setLoading(loading) {
    if (loading) {
      btnSubmitAudit.disabled = true;
      loaderBox.classList.add("active");
    } else {
      btnSubmitAudit.disabled = false;
      loaderBox.classList.remove("active");
    }
  }

  // Initial Boot in English
  setTimeout(() => {
    runPresetIncident("wheat_rust");
  }, 400);
});
