"""Language awareness and localization service for 15 Indic languages and English."""

from typing import Dict, Any, List
from app.models.common import SupportedLanguage, SeverityLevel


class LanguageMetadata:
    """Metadata descriptor for each supported language."""
    def __init__(self, code: str, name: str, native_name: str, speech_code: str, rtl: bool = False):
        self.code = code
        self.name = name
        self.native_name = native_name
        self.speech_code = speech_code
        self.rtl = rtl


SUPPORTED_LANGUAGES_REGISTRY: Dict[str, LanguageMetadata] = {
    SupportedLanguage.ASSAMESE.value: LanguageMetadata("as", "Assamese", "অসমীয়া", "as-IN"),
    SupportedLanguage.BENGALI.value: LanguageMetadata("bn", "Bengali", "বাংলা", "bn-IN"),
    SupportedLanguage.GUJARATI.value: LanguageMetadata("gu", "Gujarati", "ગુજરાતી", "gu-IN"),
    SupportedLanguage.KANNADA.value: LanguageMetadata("kn", "Kannada", "ಕನ್ನಡ", "kn-IN"),
    SupportedLanguage.KASHMIRI.value: LanguageMetadata("ks", "Kashmiri", "कॉशुर / کٲشُر", "ks-IN", rtl=True),
    SupportedLanguage.KONKANI.value: LanguageMetadata("kok", "Konkani", "कोंकणी", "kok-IN"),
    SupportedLanguage.MALAYALAM.value: LanguageMetadata("ml", "Malayalam", "മലയാളം", "ml-IN"),
    SupportedLanguage.MARATHI.value: LanguageMetadata("mr", "Marathi", "मराठी", "mr-IN"),
    SupportedLanguage.NEPALI.value: LanguageMetadata("ne", "Nepali", "नेपाली", "ne-NP"),
    SupportedLanguage.ODIA.value: LanguageMetadata("or", "Odia", "ଓଡ଼ିଆ", "or-IN"),
    SupportedLanguage.PUNJABI.value: LanguageMetadata("pa", "Punjabi", "ਪੰਜਾਬੀ", "pa-IN"),
    SupportedLanguage.SANSKRIT.value: LanguageMetadata("sa", "Sanskrit", "संस्कृतम्", "sa-IN"),
    SupportedLanguage.TAMIL.value: LanguageMetadata("ta", "Tamil", "தமிழ்", "ta-IN"),
    SupportedLanguage.TELUGU.value: LanguageMetadata("te", "Telugu", "తెలుగు", "te-IN"),
    SupportedLanguage.URDU.value: LanguageMetadata("ur", "Urdu", "اُردُو", "ur-IN", rtl=True),
    SupportedLanguage.ENGLISH.value: LanguageMetadata("en", "English", "English", "en-US"),
}

# Localized action templates and keywords per language
LOCALIZED_VOCABULARY: Dict[str, Dict[str, Any]] = {
    SupportedLanguage.ASSAMESE.value: {
        "danger_headline": "বিপদ! খেতিৰ বেমাৰ পাইছে",
        "warning_headline": "সাৱধান! শস্যৰ পাত শুকাইছে",
        "safe_headline": "শস্য সুৰক্ষিত আৰু ভালে আছে",
        "cut_leaves": "✂️ বেমাৰ লগা পাতবোৰ কাটি পুৰি পেলাওক",
        "spray_neem": "🌿 নিম তেল বা জৈৱিক ঔষধ স্প্ৰে কৰক",
        "water_advice": "💧 খেতিত অতিৰিক্ত পানী জমা হ'বলৈ নিদিব",
        "avoid_toxic": "🚫 নিষিদ্ধ ৰাসায়নিক বিষ প্ৰয়োগ নকৰিব",
        "helpline_text": "📞 বিনামূলীয়া কৃষক সহায়ক কেন্দ্ৰ: ১৫৫১",
    },
    SupportedLanguage.BENGALI.value: {
        "danger_headline": "বিপদ! ফসলে ছত্রাক আক্রমণ",
        "warning_headline": "সতর্কতা! ফসলে রোগের লক্ষণ",
        "safe_headline": "ফসল সম্পূর্ণ সুস্থ ও নিরাপদ",
        "cut_leaves": "✂️ সংক্রামিত পাতা কেটে ধ্বংস করুন",
        "spray_neem": "🌿 নিম তেল দ্রবণ স্প্রে করুন",
        "water_advice": "💧 জমিতে বাড়তি জল জমতে দেবেন না",
        "avoid_toxic": "🚫 নিষিদ্ধ বা ভেজাল বিষ ব্যবহার করবেন না",
        "helpline_text": "📞 কিসান হেল্পলাইন: ১৫৫১",
    },
    SupportedLanguage.GUJARATI.value: {
        "danger_headline": "જોખમ! પાકમાં રોગ જણાયો છે",
        "warning_headline": "ચેતવણી! પાકના પાંદડા પીળા પડ્યા",
        "safe_headline": "તમારો પાક સ્વસ્થ અને સુરક્ષિત છે",
        "cut_leaves": "✂️ રોગગ્રસ્ત પાંદડા કાપીને બાળી નાખો",
        "spray_neem": "🌿 લીમડાનું અર્ક અથવા જૈવિક દવાનો છંટકાવ કરો",
        "water_advice": "💧 ખેતરમાં વધારે પડતું પાણી ન ભરાવા દો",
        "avoid_toxic": "🚫 પ્રતિબંધિત રસાયણોનો ઉપયોગ ટાળો",
        "helpline_text": "📞 કિસાન હેલ્પલાઈન: 1551",
    },
    SupportedLanguage.KANNADA.value: {
        "danger_headline": "ಅಪಾಯ! ಬೆಳೆಯಲ್ಲಿ ರೋಗ ಬಾಧೆ",
        "warning_headline": "ಎಚ್ಚರಿಕೆ! ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ",
        "safe_headline": "ಬೆಳೆ ಆರೋಗ್ಯಕರ ಮತ್ತು ಸುರಕ್ಷಿತವಾಗಿದೆ",
        "cut_leaves": "✂️ ರೋಗಪೀಡಿತ ಎಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ ನಾಶಮಾಡಿ",
        "spray_neem": "🌿 ಬೇವಿನ ಎಣ್ಣೆ ಅಥವಾ ಸಾವಯವ ಕಷಾಯ ಸಿಂಪಡಿಸಿ",
        "water_advice": "💧 ಹೊಲದಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ",
        "avoid_toxic": "🚫 ನಿಷೇಧಿತ ಕೀಟನಾಶಕ ಬಳಸಬೇಡಿ",
        "helpline_text": "📞 ಕಿಸಾನ್ ಸಹಾಯವಾಣಿ: 1551",
    },
    SupportedLanguage.KASHMIRI.value: {
        "danger_headline": "خطرہ! فصلس لگیمژ بؠمٲرؠ",
        "warning_headline": "خبردار! پنن پؠٹھ داغ",
        "safe_headline": "فصل چھُ بالکل ٹھیک تہٕ سرسبز",
        "cut_leaves": "✂️ خراب پن کاٹِتھ الگ ترٲوِو",
        "spray_neem": "🌿 نیمک دَوا یا محفوظ سپرے کٔرِو",
        "water_advice": "💧 کھیتس منٛز آب کٹھہٕ گژھن نَہ دِیِو",
        "avoid_toxic": "🚫 خطرناک کیمیاوی زہر مَہ لٲگِو",
        "helpline_text": "📞 کسان ہیلپ لائن: ۱۵۵۱",
    },
    SupportedLanguage.KONKANI.value: {
        "danger_headline": "धोको! पिकाक दूयेंस लागलां",
        "warning_headline": "जतनाय! पानांचेर दाग आसात",
        "safe_headline": "पीक सामकें बरें आनी सुरक्षित आसा",
        "cut_leaves": "✂️ दूयेंस लागिल्लीं पानां कातरून लासून उडयात",
        "spray_neem": "🌿 कडुनिंबाचें तेल वा सेंद्रिय वखद शिंपडा",
        "water_advice": "💧 शेतांत चड उदक सांकोवंक दिव नाकात",
        "avoid_toxic": "🚫 बंद केल्लीं वायट वखदां वापरू नाकात",
        "helpline_text": "📞 शेतकार हेल्पलायन: 1551",
    },
    SupportedLanguage.MALAYALAM.value: {
        "danger_headline": "അപകടം! വിളകളിൽ ഗുരുതര രോഗം",
        "warning_headline": "ശ്രദ്ധിക്കുക! ഇലകളിൽ രോഗലക്ഷണം",
        "safe_headline": "വിള തികച്ചും ആരോഗ്യപൂർണ്ണമാണ്",
        "cut_leaves": "✂️ രോഗബാധിതമായ ഇലകൾ മുറിച്ചു മാറ്റുക",
        "spray_neem": "🌿 വേപ്പെണ്ണ മിശ്രിതം തളിക്കുക",
        "water_advice": "💧 കൃഷിയിടത്തിൽ വെള്ളം കെട്ടിക്കിടക്കരുത്",
        "avoid_toxic": "🚫 നിരോധിത കീടനാശിനികൾ ഒഴിവാക്കുക",
        "helpline_text": "📞 കിസാൻ ഹെൽപ്പ് ലൈൻ: 1551",
    },
    SupportedLanguage.MARATHI.value: {
        "danger_headline": "धोका! पिकावर बुरशीचा प्रादुर्भाव",
        "warning_headline": "सावधान! पानांवर रोगाची लक्षणे",
        "safe_headline": "पीक निरोगी आणि सुरक्षित आहे",
        "cut_leaves": "✂️ रोगट पाने तोडून शेताबाहेर नष्ट करा",
        "spray_neem": "🌿 निंबोळी अर्क किंवा जैविक औषधाची फवारणी करा",
        "water_advice": "💧 शेतात अतिरिक्त पाणी साचू देऊ नका",
        "avoid_toxic": "🚫 बंदी घातलेली विषारी औषधे वापरू नका",
        "helpline_text": "📞 किसान मदत केंद्र: 1551",
    },
    SupportedLanguage.NEPALI.value: {
        "danger_headline": "खतरा! बालीमा रोगको संक्रमण",
        "warning_headline": "सावधान! पातहरू पहेँलो हुँदैछन्",
        "safe_headline": "बाली स्वस्थ र सुरक्षित छ",
        "cut_leaves": "✂️ रोगी पातहरू काटेर जलाउनुहोस्",
        "spray_neem": "🌿 निमको तेल वा जैविक विषादी छर्कनुहोस्",
        "water_advice": "💧 खेतमा पानी जम्न नदिनुहोस्",
        "avoid_toxic": "🚫 प्रतिबन्धित विषादी प्रयोग नगर्नुहोस्",
        "helpline_text": "📞 किसान हेल्पलाइन: १५५१",
    },
    SupportedLanguage.ODIA.value: {
        "danger_headline": "ବିପଦ! ଫସଲରେ ରୋଗ ଚିହ୍ନଟ",
        "warning_headline": "ସାବଧାନ! ପତ୍ର ଶୁଖିବା ଆରମ୍ଭ ହୋଇଛି",
        "safe_headline": "ଆପଣଙ୍କ ଫସଲ ସୁସ୍ଥ ଏବଂ ନିରାପଦ ଅଛି",
        "cut_leaves": "✂️ ରୋଗାକ୍ରାନ୍ତ ପତ୍ର କାଟି ନଷ୍ଟ କରନ୍ତୁ",
        "spray_neem": "🌿 ନିମ୍ବ ତେଲ ବା ଜୈବିକ ଔଷଧ ସ୍ପ୍ରେ କରନ୍ତୁ",
        "water_advice": "💧 ଜମିରେ ଅତିରିକ୍ତ ପାଣି ଜମିବାକୁ ଦିଅନ୍ତୁ ନାହିଁ",
        "avoid_toxic": "🚫 ନିଷିଦ୍ଧ ବିଷାକ୍ତ କୀଟନାଶକ ବ୍ୟବହାର କରନ୍ତୁ ନାହିଁ",
        "helpline_text": "📞 କିଷାନ ହେଲ୍ପଲାଇନ: ୧୫୫୧",
    },
    SupportedLanguage.PUNJABI.value: {
        "danger_headline": "ਖ਼ਤਰਾ! ਫ਼ਸਲ ਉੱਤੇ ਬਿਮਾਰੀ ਦਾ ਹਮਲਾ",
        "warning_headline": "ਸਾਵਧਾਨ! ਪੱਤਿਆਂ ਉੱਤੇ ਪੀਲੇ ਦਾਗ਼",
        "safe_headline": "ਤੁਹਾਡੀ ਫ਼ਸਲ ਸਿਹਤਮੰਦ ਅਤੇ ਸੁਰੱਖਿਅਤ ਹੈ",
        "cut_leaves": "✂️ ਬਿਮਾਰ ਪੱਤਿਆਂ ਨੂੰ ਕੱਟ ਕੇ ਖੇਤੋਂ ਬਾਹਰ ਸਾੜ ਦਿਓ",
        "spray_neem": "🌿 ਨਿੰਮ ਦਾ ਤੇਲ ਜਾਂ ਜੈਵਿਕ ਦਵਾਈ ਦਾ ਛਿੜਕਾਅ ਕਰੋ",
        "water_advice": "💧 ਖੇਤ ਵਿੱਚ ਵਾਧੂ ਪਾਣੀ ਖੜ੍ਹਾ ਨਾ ਹੋਣ ਦਿਓ",
        "avoid_toxic": "🚫 ਪਾਬੰਦੀਸ਼ੁਦਾ ਜ਼ਹਿਰੀਲੀਆਂ ਦਵਾਈਆਂ ਨਾ ਵਰਤੋ",
        "helpline_text": "📞 ਕਿਸਾਨ ਹੈਲਪਲਾਈਨ: 1551",
    },
    SupportedLanguage.SANSKRIT.value: {
        "danger_headline": "सङ्कटम्! सस्ये रोगप्रसारः जातः",
        "warning_headline": "सावधानता! पर्णेषु रोगलक्षणानि दृश्यन्ते",
        "safe_headline": "सस्यं पूर्णतया स्वस्थं सुरक्षितं च अस्ति",
        "cut_leaves": "✂️ रोगग्रस्तानि पर्णानि कर्तयित्वा पृथक् कुर्वन्तु",
        "spray_neem": "🌿 निम्बसारं वा जैविकौषधं सिञ्चन्तु",
        "water_advice": "💧 क्षेत्रे अत्यधिकं जलं मा स्थापयन्तु",
        "avoid_toxic": "🚫 निषिद्धानि विषाक्तकीटनाशकानि न प्रयुञ्जताम्",
        "helpline_text": "📞 कृषकसहायताकेन्द्रम्: १५५१",
    },
    SupportedLanguage.TAMIL.value: {
        "danger_headline": "ஆபத்து! பயிரில் நோய் தாக்குதல்",
        "warning_headline": "எச்சரிக்கை! இலைகளில் பாதிப்பு",
        "safe_headline": "பயிர் ஆரோக்கியமாகவும் பாதுகாப்பாகவும் உள்ளது",
        "cut_leaves": "✂️ பாதிக்கப்பட்ட இலைகளை வெட்டி அழிக்கவும்",
        "spray_neem": "🌿 வேப்பெண்ணெய் அல்லது இயற்கை மருந்து தெளிக்கவும்",
        "water_advice": "💧 வயலில் கூடுதல் தண்ணீர் தேங்க விடாதீர்கள்",
        "avoid_toxic": "🚫 தடைசெய்யப்பட்ட பூச்சிக்கொல்லிகளை தவிர்க்கவும்",
        "helpline_text": "📞 உழவர் உதவி எண்: 1551",
    },
    SupportedLanguage.TELUGU.value: {
        "danger_headline": "ప్రమాదం! పంటకు తెగులు సోకింది",
        "warning_headline": "హెచ్చరిక! ఆకులపై మచ్చలు కనిపించాయి",
        "safe_headline": "పంట ఆరోగ్యంగా మరియు సురక్షితంగా ఉంది",
        "cut_leaves": "✂️ తెగులు సోకిన ఆకులను కత్తిరించి నాశనం చేయండి",
        "spray_neem": "🌿 వేపనూనె లేదా సేంద్రీయ మందు పిచికారీ చేయండి",
        "water_advice": "💧 పొలంలో అధిక నీరు నిల్వ ఉండకుండా చూసుకోండి",
        "avoid_toxic": "🚫 నిషేధిత విషపూరిత రసాయనాలను వాడవద్దు",
        "helpline_text": "📞 కిసాన్ కాల్ సెంటర్: 1551",
    },
    SupportedLanguage.URDU.value: {
        "danger_headline": "خطره! فصل پر بیماری کا حملہ",
        "warning_headline": "خبردار! پتوں پر زرد داغ",
        "safe_headline": "فصل بالکل تندرست اور محفوظ ہے",
        "cut_leaves": "✂️ بیمار پتوں کو کاٹ کر ضائع کر دیں",
        "spray_neem": "🌿 نیم کے تیل یا نامیاتی دوا کا اسپرے کریں",
        "water_advice": "💧 کھیت میں فالتو پانی کھڑا نہ ہونے دیں",
        "avoid_toxic": "🚫 ممنوعہ اور زہریلی ادویات سے پرہیز کریں",
        "helpline_text": "📞 کسان ہیلپ لائن: ۱۵۵۱",
    },
    SupportedLanguage.ENGLISH.value: {
        "danger_headline": "Danger! Severe Pathogen Infection",
        "warning_headline": "Warning! Early Disease Symptoms Detected",
        "safe_headline": "Crop is Healthy and Resilient",
        "cut_leaves": "✂️ Cut and destroy infected leaves immediately",
        "spray_neem": "🌿 Spray organic Neem oil or bio-fungicide",
        "water_advice": "💧 Regulate irrigation; prevent standing water",
        "avoid_toxic": "🚫 Avoid unverified synthetic toxins or banned chemicals",
        "helpline_text": "📞 Farmer Emergency Helpline: 1551",
    },
}


class LanguageService:
    """Provides language localization and helper methods."""

    @staticmethod
    def get_supported_languages() -> List[Dict[str, Any]]:
        """Return list of supported languages with codes and native scripts."""
        return [
            {
                "key": lang,
                "name": meta.name,
                "native_name": meta.native_name,
                "code": meta.code,
                "speech_code": meta.speech_code,
                "rtl": meta.rtl,
            }
            for lang, meta in SUPPORTED_LANGUAGES_REGISTRY.items()
        ]

    @staticmethod
    def get_metadata(language: str) -> LanguageMetadata:
        """Get metadata for a specific language or default to English."""
        return SUPPORTED_LANGUAGES_REGISTRY.get(
            language,
            SUPPORTED_LANGUAGES_REGISTRY[SupportedLanguage.ENGLISH.value]
        )

    @staticmethod
    def get_localized_pack(language: str) -> Dict[str, Any]:
        """Fetch pre-configured localized templates for a language."""
        return LOCALIZED_VOCABULARY.get(
            language,
            LOCALIZED_VOCABULARY[SupportedLanguage.ENGLISH.value]
        )
