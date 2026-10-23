/**
 * Enterprise Application Logic
 * Telemetry Ingestion, Gemini API Bridge, Speech Integration & Telemetry Rendering
 */

document.addEventListener("DOMContentLoaded", () => {
  // Audio Controller for Speech Synthesis
  const audioCtrl = new AudioController();

  // State
  let currentTargetLang = "Assamese";
  let currentSpeechCode = "as-IN";
  let selectedImageFile = null;
  let isListeningVoice = false;
  let recognition = null;
  let currentTelemetryData = null;

  // DOM Elements
  const langSelect = document.getElementById("lang-select");
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
  const btnSubmitAudit = document.getElementById("btn-submit-audit");
  const loaderBox = document.getElementById("loader-box");

  // Tabs
  const tabBtnFarmer = document.getElementById("tab-btn-farmer");
  const tabBtnGovt = document.getElementById("tab-btn-govt");
  const tabContentFarmer = document.getElementById("tab-content-farmer");
  const tabContentGovt = document.getElementById("tab-content-govt");

  // Telemetry Banner Metrics
  const valSeverity = document.getElementById("val-severity");
  const valRiskIndex = document.getElementById("val-risk-index");
  const valYieldLoss = document.getElementById("val-yield-loss");
  const valThreatRadius = document.getElementById("val-threat-radius");

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

  // 1. Fetch & Initialize 15 Indian Languages
  async function initLanguages() {
    try {
      const res = await fetch("/api/languages");
      if (res.ok) {
        const langs = await res.json();
        langSelect.innerHTML = "";
        langs.forEach(l => {
          const opt = document.createElement("option");
          opt.value = l.key;
          opt.dataset.speechCode = l.speech_code;
          opt.textContent = `${l.name} - ${l.native_name}`;
          langSelect.appendChild(opt);
        });

        // Set initial language
        const defaultChoice = langs[0];
        if (defaultChoice) {
          langSelect.value = defaultChoice.key;
          currentTargetLang = defaultChoice.key;
          currentSpeechCode = defaultChoice.speech_code;
        }
      }
    } catch (err) {
      console.warn("Using default language registry:", err);
    }
  }
  initLanguages();

  langSelect.addEventListener("change", (e) => {
    const selectedOpt = langSelect.options[langSelect.selectedIndex];
    currentTargetLang = e.target.value;
    currentSpeechCode = selectedOpt.dataset.speechCode || "as-IN";

    // Auto-update current incident view to new language
    if (currentTelemetryData) {
      runDiagnosisRequest();
    }
  });

  // 2. Tab Navigation
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

  // 3. Drag and Drop File Ingestion
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
      alert("Invalid format. Please select an image file.");
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

  // 4. Voice-to-Text Recognition
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
      if (symptomNotes.value) {
        symptomNotes.value += " " + transcript;
      } else {
        symptomNotes.value = transcript;
      }
      stopVoice();
    };

    recognition.onerror = () => stopVoice();
    recognition.onend = () => stopVoice();
  }

  btnVoiceToggle.addEventListener("click", () => {
    if (!recognition) {
      alert("Speech recognition is not supported in this browser. Please enter symptom notes manually.");
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

  // 5. Quick Incident Presets
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

  // 6. Manual Audit Submission
  btnSubmitAudit.addEventListener("click", () => runDiagnosisRequest());

  async function runDiagnosisRequest() {
    setLoading(true);

    try {
      let res;
      if (selectedImageFile) {
        const formData = new FormData();
        formData.append("file", selectedImageFile);
        formData.append("target_language", currentTargetLang);
        formData.append("unstructured_text", symptomNotes.value || "Field specimen leaf inspection.");
        formData.append("latitude", inputLat.value || "28.6139");
        formData.append("longitude", inputLon.value || "77.2090");

        res = await fetch("/api/diagnose/image", {
          method: "POST",
          body: formData
        });
      } else {
        const payload = {
          unstructured_text: symptomNotes.value || "Field crop foliage exhibiting pathogen symptoms.",
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

      const data = await res.json();
      renderTelemetry(data);
    } catch (err) {
      console.error("Submission error:", err);
      // Fallback to wheat rust preset if offline
      runPresetIncident("wheat_rust");
    } finally {
      setLoading(false);
    }
  }

  // 7. Render Telemetry & Farmer Action Plan
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

  function setLoading(loading) {
    if (loading) {
      btnSubmitAudit.disabled = true;
      loaderBox.classList.add("active");
    } else {
      btnSubmitAudit.disabled = false;
      loaderBox.classList.remove("active");
    }
  }

  // Initial Boot Sample
  setTimeout(() => {
    runPresetIncident("wheat_rust");
  }, 400);
});
