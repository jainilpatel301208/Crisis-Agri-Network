"""Verification service for validating crop pathogen remedies against safe practices and standards."""

from typing import List, Dict, Tuple, Any
from app.models.response_models import WeatherContext

# Banned or hazardous agrochemicals (WHO Class Ia/Ib and national bans)
BANNED_CHEMICALS = {
    "endosulfan": "Banned persistent organic pollutant causing neurological damage.",
    "monocrotophos": "Prohibited extremely hazardous organophosphate insecticide.",
    "paraquat": "Highly toxic non-selective herbicide with no known antidote.",
    "chlorpyrifos": "Restricted neurotoxin hazardous to children and pollinators.",
    "phorate": "Prohibited systemic organophosphate with high mammal toxicity.",
    "aldicarb": "Restricted carbamate pesticide with severe groundwater leaching risk.",
    "ddt": "Universally banned bio-accumulative organochlorine."
}

# Standard safe, verified agricultural remedies by pathogen type
SAFE_PRACTICE_DATABASE: Dict[str, Dict[str, Any]] = {
    "wheat_rust": {
        "organic": [
            "Apply 5% Neem Seed Kernel Extract (NSKE) at early pustule onset",
            "Spray Trichoderma viride bio-fungicide (5g per liter of water)",
            "Dust agricultural sulfur at 20-25 kg/ha in cool morning hours"
        ],
        "chemical_verified": [
            "Propiconazole 25% EC (1ml per liter water) with mandatory PPE gear only if rust index > 40%"
        ],
        "prohibited": ["Monocrotophos", "Endosulfan", "Unregistered local toxic mixes"],
        "cultural": [
            "Uproot and burn heavily sporulating leaves away from irrigation channels",
            "Maintain 30cm spacing between rows to improve canopy aeration",
            "Plant rust-resistant certified cultivars (e.g., HD-3086, DBW-187)"
        ]
    },
    "rice_blast": {
        "organic": [
            "Foliar spray of Pseudomonas fluorescens (10g/liter)",
            "Neem oil 3% formulation combined with mild soap emulsifier",
            "Apply silicon-rich compost to strengthen silica epidermal cell walls"
        ],
        "chemical_verified": [
            "Tricyclazole 75% WP (0.6g per liter water) with protective gloves and respirator"
        ],
        "prohibited": ["Paraquat", "Phorate", "Overdosed nitrogenous fertilizers (>120kg N/ha)"],
        "cultural": [
            "Avoid excessive urea / nitrogen fertilization which tenderizes leaf tissues",
            "Drain field for 48 hours to expose soil and suppress blast sporulation"
        ]
    },
    "potato_late_blight": {
        "organic": [
            "Bordeaux mixture (1% copper sulfate + hydrated lime)",
            "Copper Oxychloride 50% WP (2.5g per liter) preventative spray",
            "Bio-control with Bacillus amyloliquefaciens"
        ],
        "chemical_verified": [
            "Metalaxyl-M + Mancozeb (2.5g per liter water) during high moisture blight alerts"
        ],
        "prohibited": ["Endosulfan", "Chlorpyrifos", "Untreated sewage water"],
        "cultural": [
            "Hill up tubers with at least 10cm soil cover to prevent zoospore infection",
            "Destroy infected potato haulms 10 days prior to harvest"
        ]
    },
    "general_fungal": {
        "organic": [
            "Apply cold-pressed Neem oil (5ml/L) with bio-surfactant",
            "Spray Trichoderma harzianum bio-fungicide solution",
            "Mild baking soda (potassium bicarbonate) spray (3g/L) for foliar pH adjustment"
        ],
        "chemical_verified": [
            "Mancozeb 75% WP (2g per liter water) only with goggles and neoprene gloves"
        ],
        "prohibited": ["Banned organophosphates", "Unlabeled synthetic cocktails"],
        "cultural": [
            "Prune infected plant tissue with sterilized shears",
            "Sanitize tools in 70% alcohol between cuts"
        ]
    },
    "general_pest": {
        "organic": [
            "Install yellow and blue sticky traps (10-12 traps per acre)",
            "Foliar spray of 10,000 ppm Azadirachtin / Neem extract (2ml/L)",
            "Introduce beneficial predatory ladybird beetles or Chrysoperla carnea"
        ],
        "chemical_verified": [
            "Emamectin Benzoate 5% SG (0.4g per liter water) with certified safety mask"
        ],
        "prohibited": ["Monocrotophos", "Endosulfan", "Paraquat", "Chlorpyrifos"],
        "cultural": [
            "Handpick large caterpillar larvae in early dawn",
            "Intercrop with marigold or basil as natural insect repellents"
        ]
    }
}


class VerificationService:
    """Verifies that identified agricultural remedies strictly comply with safe farming standards."""

    @classmethod
    def verify_remedies(
        cls,
        pathogen_name: str,
        pathogen_category: str,
        proposed_remedies: List[str],
        weather: WeatherContext
    ) -> Tuple[List[str], List[str], str]:
        """
        Audit remedies, remove unsafe/banned substances, ensure organic-first hierarchy,
        and apply weather safety restrictions.

        Returns:
            Tuple of (verified_safe_remedies, prohibited_treatments, audit_status)
        """
        # Determine closest knowledge key
        name_lower = pathogen_name.lower()
        if "rust" in name_lower or "puccinia" in name_lower:
            key = "wheat_rust"
        elif "blast" in name_lower or "magnaporthe" in name_lower:
            key = "rice_blast"
        elif "blight" in name_lower or "phytophthora" in name_lower:
            key = "potato_late_blight"
        elif pathogen_category == "PEST_INSECT" or "aphid" in name_lower or "borer" in name_lower:
            key = "general_pest"
        else:
            key = "general_fungal"

        db_entry = SAFE_PRACTICE_DATABASE[key]

        # Scan for banned chemicals in proposed remedies
        prohibited_list = list(db_entry["prohibited"])
        cleaned_proposed: List[str] = []

        for remedy in proposed_remedies:
            is_banned = False
            for banned_word, reason in BANNED_CHEMICALS.items():
                if banned_word in remedy.lower():
                    is_banned = True
                    prohibited_list.append(f"{banned_word.capitalize()} ({reason})")
                    break
            if not is_banned:
                cleaned_proposed.append(remedy)

        # Build prioritized verified list: Organic First, Cultural Second, Verified Chemicals Third
        verified_safe: List[str] = []

        # 1. Add organic remedies
        for org in db_entry["organic"]:
            verified_safe.append(f"🌿 [Organic/Safe]: {org}")

        # 2. Add cultural practices
        for cult in db_entry["cultural"]:
            verified_safe.append(f"✂️ [Cultural Best Practice]: {cult}")

        # 3. Add approved chemical (with mandatory safety caution)
        for chem in db_entry["chemical_verified"]:
            verified_safe.append(f"🛡️ [Regulated Chemical - Wear PPE]: {chem}")

        # Integrate clean proposed remedies that aren't duplicates
        for item in cleaned_proposed:
            if not any(item.lower()[:15] in v.lower() for v in verified_safe):
                verified_safe.append(f"✅ [Verified Advisory]: {item}")

        # Weather constraint override
        audit_status = "VERIFIED_SAFE_ORGANIC_FIRST"
        if weather.precipitation_probability_pct > 60:
            verified_safe.insert(
                0,
                f"⚠️ [Weather Override]: Rainfall risk is {weather.precipitation_probability_pct}%. Postpone foliar spraying to prevent chemical runoff into water sources."
            )
            audit_status = "VERIFIED_HOLD_DUE_TO_RAIN"
        elif weather.wind_speed_kmh > 18:
            verified_safe.insert(
                0,
                f"⚠️ [Weather Override]: Wind speed is {weather.wind_speed_kmh} km/h. Postpone spraying to prevent hazardous pesticide drift to adjacent fields."
            )
            audit_status = "VERIFIED_HOLD_DUE_TO_WIND"

        # Deduplicate prohibited list while preserving order
        unique_prohibited = list(dict.fromkeys(prohibited_list))

        return verified_safe, unique_prohibited, audit_status
