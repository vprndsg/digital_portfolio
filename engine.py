from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping
from zoneinfo import ZoneInfo

from skyfield import almanac
from skyfield.api import Topos, load


BASE_DIR = Path(__file__).resolve().parent
EPHEMERIS_PATH = BASE_DIR / "data" / "de421.bsp"

LOS_ANGELES = ZoneInfo("America/Los_Angeles")
TIMESCALE = load.timescale()
EPHEMERIS = load(str(EPHEMERIS_PATH))
EARTH = EPHEMERIS["earth"]
MOON = EPHEMERIS["moon"]
SUN = EPHEMERIS["sun"]
OBSERVER = Topos("36.9741 N", "122.0308 W")

VALID_PARTY_MODES = {"solo", "pair", "crowd"}
VALID_APPETITES = {"comfort", "electric", "curious"}
DEFAULT_BOTTLE_PROFILE = "none"
CUSTOM_BOTTLE_PROFILE = "custom"

VALID_CUSTOM_COLORS = {"red", "rose", "white", "orange"}
VALID_CUSTOM_SPARKLES = {"still", "pet_nat", "sparkling"}
VALID_CUSTOM_BODIES = {"light", "medium", "full"}

DEFAULT_CUSTOM_BOTTLE = {
    "name": "House bottle",
    "color": "red",
    "sparkle": "still",
    "body": "medium",
    "acid": 3,
    "aroma": 3,
    "savor": 3,
    "fruit": 3,
}

LEVEL_SHIFT = {1: -16, 2: -8, 3: 0, 4: 8, 5: 16}

CUSTOM_COLOR_TRAITS = {
    "red": {"fruit": 70, "floral": 34, "herbal": 28, "mineral": 44, "texture": 64, "acid": 56, "intensity": 70},
    "rose": {"fruit": 66, "floral": 50, "herbal": 24, "mineral": 36, "texture": 42, "acid": 70, "intensity": 56},
    "white": {"fruit": 46, "floral": 48, "herbal": 42, "mineral": 56, "texture": 30, "acid": 74, "intensity": 48},
    "orange": {"fruit": 52, "floral": 42, "herbal": 54, "mineral": 60, "texture": 66, "acid": 58, "intensity": 68},
}

CUSTOM_COLOR_AFFINITIES = {
    "red": ["Fire", "Earth"],
    "rose": ["Fire", "Air"],
    "white": ["Water", "Air"],
    "orange": ["Air", "Earth"],
}

SPARKLE_MODIFIERS = {
    "still": {"fruit": 0, "floral": 0, "texture": 0, "acid": 0, "intensity": 0},
    "pet_nat": {"fruit": 6, "floral": 6, "texture": -6, "acid": 8, "intensity": -2},
    "sparkling": {"fruit": 4, "floral": 10, "texture": -10, "acid": 14, "intensity": -6},
}

BODY_MODIFIERS = {
    "light": {"texture": -12, "intensity": -10, "acid": 4, "fruit": 2, "mineral": -4},
    "medium": {"texture": 0, "intensity": 0, "acid": 0, "fruit": 0, "mineral": 0},
    "full": {"texture": 14, "intensity": 12, "acid": -4, "fruit": 4, "mineral": 8},
}

CUSTOM_BODY_APPETITES = {
    "light": ["electric", "curious"],
    "medium": ["comfort", "curious"],
    "full": ["comfort", "curious"],
}

AXIS_UPSHIFT_NOTES = {
    "fruit": "Add hot honey, char, or sweeter onion to make fruit feel louder.",
    "floral": "Bring basil, fennel pollen, citrus zest, or a more aromatic glass.",
    "herbal": "Lean on parsley, bitter greens, olive oil, or soft green herbs.",
    "mineral": "Use anchovy, caper, olive, or deeper crust char to add stone and salt.",
    "texture": "Choose creamier cheese, slower pours, and a warmer serving temperature.",
    "acid": "Serve colder and bring pickled peppers, lemon, or vinegar into the plate.",
    "intensity": "Pour a smaller glass first and give the room a sharper savory cue.",
}

AXIS_DOWNSHIFT_NOTES = {
    "fruit": "Bring more salt and smoke so the bottle does not feel candied.",
    "floral": "Skip the perfumed garnish and let the crust and cheese do more work.",
    "herbal": "Reduce green garnish and keep the plate warmer, softer, and rounder.",
    "mineral": "Drop the brine and go softer on char so the bottle feels less severe.",
    "texture": "Open a touch colder and pair with brighter toppings to cut through weight.",
    "acid": "Use creamier elements and less citrus so the bottle stops shouting.",
    "intensity": "Give it more air and a fuller bite before the next serious sip.",
}

DAY_TYPE_BY_SIGN = {
    "Aries": ("Fruit Day", "Fire"),
    "Leo": ("Fruit Day", "Fire"),
    "Sagittarius": ("Fruit Day", "Fire"),
    "Gemini": ("Flower Day", "Air"),
    "Libra": ("Flower Day", "Air"),
    "Aquarius": ("Flower Day", "Air"),
    "Cancer": ("Leaf Day", "Water"),
    "Scorpio": ("Leaf Day", "Water"),
    "Pisces": ("Leaf Day", "Water"),
    "Taurus": ("Root Day", "Earth"),
    "Virgo": ("Root Day", "Earth"),
    "Capricorn": ("Root Day", "Earth"),
}

PHASE_NAME_BY_INDEX = {
    0: "New Moon",
    1: "First Quarter",
    2: "Full Moon",
    3: "Last Quarter",
}

PHASE_ARC_BY_PHASE = {
    "New Moon": "Seed",
    "Waxing Crescent": "Seed",
    "First Quarter": "Charge",
    "Waxing Gibbous": "Charge",
    "Full Moon": "Peak",
    "Waning Gibbous": "Release",
    "Last Quarter": "Release",
    "Waning Crescent": "Release",
}

SIGNAL_NAME = {
    ("Fire", "Seed"): "Sparkstarter",
    ("Fire", "Charge"): "Oven Pulse",
    ("Fire", "Peak"): "Cinder Parade",
    ("Fire", "Release"): "Low Ember",
    ("Air", "Seed"): "Glass Bloom",
    ("Air", "Charge"): "Silver Drift",
    ("Air", "Peak"): "Neon Bouquet",
    ("Air", "Release"): "Soft Static",
    ("Water", "Seed"): "Green Tide",
    ("Water", "Charge"): "Salt Lift",
    ("Water", "Peak"): "Velvet Current",
    ("Water", "Release"): "Moss Reverie",
    ("Earth", "Seed"): "Stone Seed",
    ("Earth", "Charge"): "Kiln Line",
    ("Earth", "Peak"): "Granite Chorus",
    ("Earth", "Release"): "Cellar Quiet",
}

PALETTE_BY_ELEMENT = {
    "Fire": {
        "primary": "#d46b3b",
        "secondary": "#f4d8b8",
        "glow": "rgba(212, 107, 59, 0.34)",
    },
    "Air": {
        "primary": "#5a86a8",
        "secondary": "#d9e8ef",
        "glow": "rgba(90, 134, 168, 0.28)",
    },
    "Water": {
        "primary": "#3d7868",
        "secondary": "#d8eadf",
        "glow": "rgba(61, 120, 104, 0.28)",
    },
    "Earth": {
        "primary": "#7a6650",
        "secondary": "#ece0cf",
        "glow": "rgba(122, 102, 80, 0.28)",
    },
}

BASE_SCORES = {
    "Fire": {"fruit": 82, "floral": 38, "herbal": 22, "mineral": 35, "texture": 58, "acid": 64, "social": 78},
    "Air": {"fruit": 48, "floral": 85, "herbal": 28, "mineral": 42, "texture": 33, "acid": 72, "social": 66},
    "Water": {"fruit": 40, "floral": 45, "herbal": 80, "mineral": 36, "texture": 61, "acid": 51, "social": 42},
    "Earth": {"fruit": 35, "floral": 28, "herbal": 44, "mineral": 84, "texture": 76, "acid": 46, "social": 52},
}

ARC_MODIFIERS = {
    "Seed": {"fruit": 4, "floral": 6, "herbal": 2, "mineral": -2, "texture": -6, "acid": 8, "social": -4, "intensity": 46},
    "Charge": {"fruit": 8, "floral": 4, "herbal": 0, "mineral": 2, "texture": 3, "acid": 5, "social": 6, "intensity": 67},
    "Peak": {"fruit": 10, "floral": 8, "herbal": 4, "mineral": 1, "texture": 7, "acid": 1, "social": 12, "intensity": 84},
    "Release": {"fruit": -6, "floral": -3, "herbal": 6, "mineral": 8, "texture": 10, "acid": -4, "social": -8, "intensity": 58},
}

MOTION_MODIFIERS = {
    "Ascending": {"fruit": 0, "floral": 8, "herbal": 0, "mineral": 0, "texture": -3, "acid": 4, "social": 4, "intensity": 3},
    "Descending": {"fruit": 0, "floral": 0, "herbal": 2, "mineral": 6, "texture": 5, "acid": 0, "social": -2, "intensity": -2},
}

PIZZA_PLAN = {
    "Fire": {
        "comfort": {"name": "Pepperoni, roasted red onion, hot honey", "note": "A bright, high-heat pie that keeps fruit in the front seat."},
        "electric": {"name": "Nduja, pickled peppers, mozzarella", "note": "Punchy spice and acid to keep the room moving."},
        "curious": {"name": "Fennel sausage, charred apricot, pecorino", "note": "Sweet smoke and savory lift in the same bite."},
    },
    "Air": {
        "comfort": {"name": "Ricotta, lemon zest, basil", "note": "Soft edges, perfume on the nose, and a clean finish."},
        "electric": {"name": "Squash blossom, fresh mozzarella, chili oil", "note": "Fast aromatics, light hands, bright detail."},
        "curious": {"name": "Shallot cream, maitake, tarragon", "note": "An airy pie with enough weirdness to stay memorable."},
    },
    "Water": {
        "comfort": {"name": "Pesto, zucchini, stracciatella", "note": "Green, cool, and easy on the first sip."},
        "electric": {"name": "Green olive, anchovy, parsley", "note": "Brine and herbs to sharpen the tasting angle."},
        "curious": {"name": "Broccolini, caper, preserved lemon", "note": "Leafy tension with salty little detonations."},
    },
    "Earth": {
        "comfort": {"name": "Mushroom, fontina, thyme", "note": "Deep and warm, tuned for structure and slow savoriness."},
        "electric": {"name": "Potato, rosemary, taleggio", "note": "Starch and funk to make mineral tones feel louder."},
        "curious": {"name": "Sunchoke, onion jam, smoked scamorza", "note": "Cellar energy in pizza form."},
    },
}

WINE_PLAN = {
    "Fire": {
        "comfort": {"name": "Lambrusco Grasparossa", "note": "Serve cool. Let the fizz scrub the palate between hot bites."},
        "electric": {"name": "Chilled Frappato", "note": "Bright red fruit, easy pace, no heavy hand needed."},
        "curious": {"name": "Etna Rosso", "note": "For when you want smoke, lift, and volcanic snap in the same glass."},
    },
    "Air": {
        "comfort": {"name": "Dry sparkling rose", "note": "Open cold and pour small; this is an aromatic day."},
        "electric": {"name": "Skin-contact Malvasia", "note": "Aromatics first, texture second, conversation third."},
        "curious": {"name": "Savagnin or another high-tone aromatic field blend", "note": "Lean into odd detail and perfume."},
    },
    "Water": {
        "comfort": {"name": "Verdicchio", "note": "Cool, herbal, and just structured enough to keep shape."},
        "electric": {"name": "Txakoli", "note": "Salt, acid, and velocity are the point."},
        "curious": {"name": "Assyrtiko", "note": "Herbs and tension without giving up backbone."},
    },
    "Earth": {
        "comfort": {"name": "Barbera d'Asti", "note": "Enough acid to move, enough depth to stay grounded."},
        "electric": {"name": "Cerasuolo d'Abruzzo", "note": "A darker rose that still keeps its feet moving."},
        "curious": {"name": "Blaufrankisch", "note": "Mineral, peppery, and built for serious slices."},
    },
}

SIDE_PLAN = {
    "Fire": "Charred broccolini with chile salt",
    "Air": "Fennel and citrus salad",
    "Water": "Celery, herbs, and briny olives",
    "Earth": "Warm mushrooms with white beans and rosemary",
}

SOUNDTRACK = {
    "Fire": {"base": "Italo disco and garage soul", "Seed": "keep it punchy but not loud", "Charge": "let the groove drive dinner", "Peak": "turn the room into a low-stakes celebration", "Release": "switch to late-night burners"},
    "Air": {"base": "dream pop and light synth", "Seed": "play the airy cuts first", "Charge": "bring in more shimmer", "Peak": "go bright and cinematic", "Release": "fade to suspended chords"},
    "Water": {"base": "dub, ambient, and slow percussion", "Seed": "keep the rhythm soft", "Charge": "let the bassline enter slowly", "Peak": "go deeper without getting heavy", "Release": "end with drifting instrumentals"},
    "Earth": {"base": "jazz-funk and smoky post-punk", "Seed": "set a grounded pulse", "Charge": "tighten the groove", "Peak": "bring in something with spine", "Release": "slow the room down"},
}

RITUALS = {
    ("Ascending", "Seed"): {"title": "Open before the oven does", "note": "Pour the first sip while the dough warms. This is a lift-off day."},
    ("Ascending", "Charge"): {"title": "Catch the first aromatic wave", "note": "Let the first pour happen standing up, before anyone settles in."},
    ("Ascending", "Peak"): {"title": "Golden-hour first glass", "note": "This is the version of the bottle that wants a room to notice it."},
    ("Ascending", "Release"): {"title": "Late bloom", "note": "Do not rush the first judgment. Give the glass a little air and re-check."},
    ("Descending", "Seed"): {"title": "Build the base", "note": "Salt the food first, pour second. Ground the palate before the first sip."},
    ("Descending", "Charge"): {"title": "Decant with intent", "note": "Ten to fifteen minutes of air will make the room feel more focused."},
    ("Descending", "Peak"): {"title": "Anchor the room", "note": "Serve something savory first so the bottle lands with more weight."},
    ("Descending", "Release"): {"title": "Cellar hour", "note": "Lower the lights, slow the pace, and let the bottle come to you."},
}

PARTY_MOVES = {
    "solo": {"title": "Solo service", "note": "One record, one pizza, one bottle. The point is noticing changes, not maximizing choices."},
    "pair": {"title": "Two-glass conversation", "note": "Pour smaller than usual and compare impressions out loud after the first slice."},
    "crowd": {"title": "Host move", "note": "Lead with the lighter bottle, save the darker or stranger wine for when the room is warmed up."},
}

APPETITE_WEIGHT = {
    "comfort": {"fruit": 0.14, "floral": 0.05, "herbal": 0.15, "mineral": 0.10, "texture": 0.28, "acid": 0.10, "social": 0.05, "intensity": 0.13},
    "electric": {"fruit": 0.22, "floral": 0.12, "herbal": 0.05, "mineral": 0.05, "texture": 0.08, "acid": 0.18, "social": 0.15, "intensity": 0.15},
    "curious": {"fruit": 0.12, "floral": 0.16, "herbal": 0.10, "mineral": 0.20, "texture": 0.10, "acid": 0.10, "social": 0.03, "intensity": 0.19},
}

AXIS_LABELS = {
    "fruit": "Fruit",
    "floral": "Floral",
    "herbal": "Herbal",
    "mineral": "Mineral",
    "texture": "Texture",
    "acid": "Acid",
    "social": "Social",
    "intensity": "Intensity",
}

BOTTLE_PROFILES = {
    "none": {
        "name": "No specific bottle selected",
        "traits": {},
        "note": "Use the generic signal and archetype recommendations.",
        "affinities": [],
        "appetite_bias": [],
    },
    "custom": {
        "name": "Build a bottle blueprint",
        "traits": {},
        "note": "Describe your own bottle and test it against the week.",
        "affinities": [],
        "appetite_bias": [],
    },
    "lambrusco": {
        "name": "Bubbly red / Lambrusco lane",
        "traits": {"fruit": 84, "floral": 34, "herbal": 22, "mineral": 28, "texture": 32, "acid": 80, "intensity": 66},
        "note": "For nights where fizz, sauce, and velocity matter more than gravitas.",
        "affinities": ["Fire"],
        "appetite_bias": ["comfort", "electric"],
    },
    "volcanic_red": {
        "name": "Volcanic lifted red",
        "traits": {"fruit": 58, "floral": 48, "herbal": 36, "mineral": 82, "texture": 54, "acid": 70, "intensity": 72},
        "note": "Smoke, mineral detail, and enough brightness to keep a slice honest.",
        "affinities": ["Fire", "Earth"],
        "appetite_bias": ["curious"],
    },
    "coastal_white": {
        "name": "Salty coastal white",
        "traits": {"fruit": 44, "floral": 40, "herbal": 58, "mineral": 78, "texture": 38, "acid": 76, "intensity": 52},
        "note": "Built for brine, herbs, and clean finishes.",
        "affinities": ["Water", "Air"],
        "appetite_bias": ["electric", "curious"],
    },
    "skin_contact": {
        "name": "Skin-contact / orange wine",
        "traits": {"fruit": 50, "floral": 64, "herbal": 44, "mineral": 62, "texture": 68, "acid": 58, "intensity": 74},
        "note": "A textural bottle when aroma and savory edges both matter.",
        "affinities": ["Air", "Earth"],
        "appetite_bias": ["curious"],
    },
    "rose_depth": {
        "name": "Serious rose",
        "traits": {"fruit": 70, "floral": 52, "herbal": 30, "mineral": 46, "texture": 48, "acid": 72, "intensity": 60},
        "note": "Somewhere between aperitivo and dinner-table authority.",
        "affinities": ["Fire", "Air"],
        "appetite_bias": ["comfort", "electric"],
    },
    "forest_red": {
        "name": "Earthy cellar red",
        "traits": {"fruit": 36, "floral": 24, "herbal": 52, "mineral": 86, "texture": 78, "acid": 48, "intensity": 70},
        "note": "For mushroom pies, mineral days, and slow pours.",
        "affinities": ["Earth"],
        "appetite_bias": ["comfort", "curious"],
    },
    "aromatic_white": {
        "name": "Aromatic lifted white",
        "traits": {"fruit": 54, "floral": 84, "herbal": 32, "mineral": 40, "texture": 26, "acid": 74, "intensity": 56},
        "note": "High-tone, perfumed, and happiest when the room is still light on its feet.",
        "affinities": ["Air"],
        "appetite_bias": ["electric", "curious"],
    },
}


@dataclass(frozen=True)
class LunarState:
    day: date
    moon_phase: str
    phase_arc: str
    zodiac_sign: str
    day_type: str
    element: str
    motion: str
    signal_name: str


def coerce_level(value: Any, default: int = 3) -> int:
    try:
        level = int(value)
    except (TypeError, ValueError):
        return default
    return max(1, min(5, level))


def clean_text(value: Any, fallback: str, max_length: int = 48) -> str:
    if not isinstance(value, str):
        return fallback
    cleaned = " ".join(value.strip().split())
    if not cleaned:
        return fallback
    return cleaned[:max_length]


def mapping_value(payload: Mapping[str, Any] | None, *keys: str) -> Any:
    if payload is None:
        return None
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def normalize_custom_bottle(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    color = mapping_value(payload, "custom_color", "color")
    sparkle = mapping_value(payload, "custom_sparkle", "sparkle")
    body = mapping_value(payload, "custom_body", "body")

    normalized = {
        "name": clean_text(mapping_value(payload, "custom_name", "name"), DEFAULT_CUSTOM_BOTTLE["name"], max_length=60),
        "color": color if color in VALID_CUSTOM_COLORS else DEFAULT_CUSTOM_BOTTLE["color"],
        "sparkle": sparkle if sparkle in VALID_CUSTOM_SPARKLES else DEFAULT_CUSTOM_BOTTLE["sparkle"],
        "body": body if body in VALID_CUSTOM_BODIES else DEFAULT_CUSTOM_BOTTLE["body"],
        "acid": coerce_level(mapping_value(payload, "custom_acid", "acid"), DEFAULT_CUSTOM_BOTTLE["acid"]),
        "aroma": coerce_level(mapping_value(payload, "custom_aroma", "aroma"), DEFAULT_CUSTOM_BOTTLE["aroma"]),
        "savor": coerce_level(mapping_value(payload, "custom_savor", "savor"), DEFAULT_CUSTOM_BOTTLE["savor"]),
        "fruit": coerce_level(mapping_value(payload, "custom_fruit", "fruit"), DEFAULT_CUSTOM_BOTTLE["fruit"]),
    }
    return normalized


def adjust_traits(base: dict[str, int], modifiers: Mapping[str, int]) -> None:
    for axis, change in modifiers.items():
        base[axis] = clamp(base[axis] + change)


def custom_style_line(config: Mapping[str, Any]) -> str:
    sparkle_label = {
        "still": "still",
        "pet_nat": "pet-nat",
        "sparkling": "sparkling",
    }[str(config["sparkle"])]
    body_label = {
        "light": "light-bodied",
        "medium": "mid-weight",
        "full": "full-bodied",
    }[str(config["body"])]
    color_label = {
        "red": "red",
        "rose": "rose",
        "white": "white",
        "orange": "orange",
    }[str(config["color"])]
    return f"{body_label} {sparkle_label} {color_label}"


def build_custom_profile(config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    custom = normalize_custom_bottle(config)
    traits = dict(CUSTOM_COLOR_TRAITS[custom["color"]])
    adjust_traits(traits, SPARKLE_MODIFIERS[custom["sparkle"]])
    adjust_traits(traits, BODY_MODIFIERS[custom["body"]])

    aroma_shift = LEVEL_SHIFT[custom["aroma"]]
    savor_shift = LEVEL_SHIFT[custom["savor"]]
    fruit_shift = LEVEL_SHIFT[custom["fruit"]]
    acid_shift = LEVEL_SHIFT[custom["acid"]]

    traits["acid"] = clamp(traits["acid"] + acid_shift)
    traits["floral"] = clamp(traits["floral"] + aroma_shift)
    traits["herbal"] = clamp(traits["herbal"] + int(round(savor_shift * 0.7)))
    traits["mineral"] = clamp(traits["mineral"] + savor_shift)
    traits["texture"] = clamp(traits["texture"] + int(round(savor_shift * 0.5)))
    traits["fruit"] = clamp(traits["fruit"] + fruit_shift)
    traits["intensity"] = clamp(traits["intensity"] + int(round((fruit_shift + savor_shift) / 3)))

    appetite_bias = set(CUSTOM_BODY_APPETITES[custom["body"]])
    if custom["sparkle"] != "still":
        appetite_bias.add("electric")
    if custom["fruit"] >= 4:
        appetite_bias.add("comfort")
    if custom["savor"] >= 4 or custom["color"] == "orange":
        appetite_bias.add("curious")

    style_line = custom_style_line(custom)
    note = (
        f"{style_line.capitalize()} with acid {custom['acid']}/5, aroma {custom['aroma']}/5, "
        f"savor {custom['savor']}/5, and fruit {custom['fruit']}/5."
    )
    return {
        "key": CUSTOM_BOTTLE_PROFILE,
        "name": clean_text(custom["name"], DEFAULT_CUSTOM_BOTTLE["name"], max_length=60),
        "traits": traits,
        "note": note,
        "affinities": CUSTOM_COLOR_AFFINITIES[custom["color"]],
        "appetite_bias": sorted(appetite_bias),
        "custom_config": custom,
        "style_line": style_line,
    }


def resolve_selected_profile(profile_key: str, custom_bottle: Mapping[str, Any] | None = None) -> dict[str, Any]:
    if profile_key == CUSTOM_BOTTLE_PROFILE:
        return build_custom_profile(custom_bottle)

    profile = BOTTLE_PROFILES.get(profile_key, BOTTLE_PROFILES[DEFAULT_BOTTLE_PROFILE])
    return {
        "key": profile_key if profile_key in BOTTLE_PROFILES else DEFAULT_BOTTLE_PROFILE,
        "name": profile["name"],
        "traits": dict(profile["traits"]),
        "note": profile["note"],
        "affinities": list(profile["affinities"]),
        "appetite_bias": list(profile["appetite_bias"]),
        "style_line": profile["note"],
        "custom_config": normalize_custom_bottle(custom_bottle),
    }


def normalize_party_mode(value: str | None) -> str:
    if value in VALID_PARTY_MODES:
        return value
    return "pair"


def normalize_appetite(value: str | None) -> str:
    if value in VALID_APPETITES:
        return value
    return "curious"


def normalize_bottle_profile(value: str | None) -> str:
    if value in BOTTLE_PROFILES:
        return value
    return DEFAULT_BOTTLE_PROFILE


def parse_date(value: str | None) -> date:
    if not value:
        return datetime.now(LOS_ANGELES).date()
    try:
        return date.fromisoformat(value)
    except ValueError:
        return datetime.now(LOS_ANGELES).date()


def as_local_datetime(day: date) -> datetime:
    return datetime.combine(day, datetime.min.time(), tzinfo=LOS_ANGELES)


def clamp(value: int) -> int:
    return max(0, min(100, value))


def detect_phase(day: date) -> str:
    local_dt = as_local_datetime(day)
    utc_dt = local_dt.astimezone(timezone.utc)
    t0 = TIMESCALE.utc(utc_dt.year, utc_dt.month, utc_dt.day)
    t1 = TIMESCALE.utc((utc_dt + timedelta(days=1)).year, (utc_dt + timedelta(days=1)).month, (utc_dt + timedelta(days=1)).day)
    times, phases = almanac.find_discrete(t0, t1, almanac.moon_phases(EPHEMERIS))
    if len(phases):
        return PHASE_NAME_BY_INDEX[int(phases[0])]

    midday = utc_dt + timedelta(hours=12)
    t = TIMESCALE.utc(midday.year, midday.month, midday.day, midday.hour, midday.minute)
    earth_view = EARTH.at(t)
    _, sun_lon, _ = earth_view.observe(SUN).apparent().ecliptic_latlon()
    _, moon_lon, _ = earth_view.observe(MOON).apparent().ecliptic_latlon()
    angle = (moon_lon.degrees - sun_lon.degrees) % 360
    if angle < 90:
        return "Waxing Crescent"
    if angle < 180:
        return "Waxing Gibbous"
    if angle < 270:
        return "Waning Gibbous"
    return "Waning Crescent"


def moon_zodiac_sign(day: date) -> str:
    local_dt = as_local_datetime(day)
    utc_dt = local_dt.astimezone(timezone.utc)
    t = TIMESCALE.utc(utc_dt.year, utc_dt.month, utc_dt.day, 12)
    _, lon, _ = EARTH.at(t).observe(MOON).apparent().ecliptic_latlon()
    zodiac_signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    index = int(lon.degrees % 360 // 30)
    return zodiac_signs[index]


def moon_motion(day: date) -> str:
    local_dt = as_local_datetime(day)
    utc_dt = local_dt.astimezone(timezone.utc)
    t_today = TIMESCALE.utc(utc_dt.year, utc_dt.month, utc_dt.day, 12)
    tomorrow_dt = utc_dt + timedelta(days=1)
    t_tomorrow = TIMESCALE.utc(tomorrow_dt.year, tomorrow_dt.month, tomorrow_dt.day, 12)
    moon_lat_today = EARTH.at(t_today).observe(MOON).apparent().ecliptic_latlon()[0].degrees
    moon_lat_tomorrow = EARTH.at(t_tomorrow).observe(MOON).apparent().ecliptic_latlon()[0].degrees
    return "Ascending" if moon_lat_tomorrow > moon_lat_today else "Descending"


@lru_cache(maxsize=None)
def build_lunar_state(day: date) -> LunarState:
    moon_phase = detect_phase(day)
    phase_arc = PHASE_ARC_BY_PHASE[moon_phase]
    zodiac_sign = moon_zodiac_sign(day)
    day_type, element = DAY_TYPE_BY_SIGN[zodiac_sign]
    motion = moon_motion(day)
    signal_name = SIGNAL_NAME[(element, phase_arc)]
    return LunarState(
        day=day,
        moon_phase=moon_phase,
        phase_arc=phase_arc,
        zodiac_sign=zodiac_sign,
        day_type=day_type,
        element=element,
        motion=motion,
        signal_name=signal_name,
    )


def score_axes(state: LunarState) -> dict[str, int]:
    base = BASE_SCORES[state.element]
    arc = ARC_MODIFIERS[state.phase_arc]
    motion = MOTION_MODIFIERS[state.motion]
    scores = {
        axis: clamp(base[axis] + arc.get(axis, 0) + motion.get(axis, 0))
        for axis in ("fruit", "floral", "herbal", "mineral", "texture", "acid", "social")
    }
    scores["intensity"] = clamp(arc["intensity"] + motion.get("intensity", 0))
    return scores


def dominant_axes(scores: dict[str, int], count: int = 3) -> list[dict[str, Any]]:
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [{"key": key, "label": AXIS_LABELS[key], "value": value} for key, value in ranked[:count]]


def profile_fit_detail(
    profile: Mapping[str, Any],
    scores: dict[str, int],
    state: LunarState,
    appetite: str,
    party_mode: str,
) -> dict[str, Any]:
    profile_key = str(profile["key"])
    if profile_key == DEFAULT_BOTTLE_PROFILE:
        return {
            "key": profile_key,
            "name": profile["name"],
            "score": None,
            "note": profile["note"],
            "aligned_axes": [],
            "tension_axes": [],
        }

    diffs = {
        axis: abs(int(profile["traits"][axis]) - scores[axis])
        for axis in ("fruit", "floral", "herbal", "mineral", "texture", "acid", "intensity")
    }
    average_diff = sum(diffs.values()) / len(diffs)
    score = 100 - (average_diff * 1.18)
    if state.element in profile.get("affinities", []):
        score += 4
    if appetite in profile.get("appetite_bias", []):
        score += 3
    if party_mode == "crowd" and profile_key in {"lambrusco", "rose_depth"}:
        score += 3
    if party_mode == "solo" and profile_key in {"forest_red", "skin_contact", "volcanic_red", CUSTOM_BOTTLE_PROFILE}:
        score += 2

    aligned = sorted(diffs.items(), key=lambda item: item[1])[:2]
    tension = sorted(diffs.items(), key=lambda item: item[1], reverse=True)[:2]
    aligned_axes = [{"key": key, "label": AXIS_LABELS[key], "gap": gap} for key, gap in aligned]
    tension_axes = [{"key": key, "label": AXIS_LABELS[key], "gap": gap} for key, gap in tension]

    if score >= 80:
        fit_note = "Excellent fit for the signal."
    elif score >= 68:
        fit_note = "Strong fit if this is the bottle you want to make the night about."
    elif score >= 55:
        fit_note = "Usable, but not the cleanest expression of the signal."
    else:
        fit_note = "Probably save this for a better night."

    return {
        "key": profile_key,
        "name": profile["name"],
        "score": clamp(int(round(score))),
        "note": f"{fit_note} {profile['note']}",
        "aligned_axes": aligned_axes,
        "tension_axes": tension_axes,
    }


def top_profile_matches(
    scores: dict[str, int],
    state: LunarState,
    appetite: str,
    party_mode: str,
    count: int = 3,
) -> list[dict[str, Any]]:
    ranked = []
    for profile_key in BOTTLE_PROFILES:
        if profile_key in {DEFAULT_BOTTLE_PROFILE, CUSTOM_BOTTLE_PROFILE}:
            continue
        ranked.append(
            profile_fit_detail(
                resolve_selected_profile(profile_key),
                scores,
                state,
                appetite,
                party_mode,
            )
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:count]


def bottle_score(scores: dict[str, int], appetite: str, party_mode: str) -> float:
    weight = APPETITE_WEIGHT[appetite].copy()
    if party_mode == "crowd":
        weight["social"] += 0.06
        weight["texture"] -= 0.02
        weight["mineral"] -= 0.02
        weight["intensity"] -= 0.02
    if party_mode == "solo":
        weight["texture"] += 0.03
        weight["mineral"] += 0.02
        weight["social"] -= 0.04
        weight["fruit"] -= 0.01
    return round(sum(scores[key] * value for key, value in weight.items()), 1)


def compose_thesis(state: LunarState, scores: dict[str, int]) -> str:
    if state.element == "Fire":
        focus = "char, brightness, and a bottle with swagger"
    elif state.element == "Air":
        focus = "aroma, lift, and details that hover over the crust"
    elif state.element == "Water":
        focus = "green edges, saline detail, and softer pacing"
    else:
        focus = "stone, depth, and savory weight"

    if state.phase_arc == "Seed":
        movement = "start fresh and keep the first sip curious"
    elif state.phase_arc == "Charge":
        movement = "push forward and build momentum through dinner"
    elif state.phase_arc == "Peak":
        movement = "go broad, expressive, and slightly theatrical"
    else:
        movement = "slow down, let the bottle settle, and notice the aftertaste"

    texture_line = "Stay nimble." if scores["texture"] < 50 else "Let the texture linger."
    return f"{state.signal_name} is a {state.phase_arc.lower()} {state.element.lower()} signal: lean into {focus}. Tonight wants you to {movement}. {texture_line}"


def opening_window(state: LunarState) -> dict[str, str]:
    matrix = {
        ("Ascending", "Seed"): ("First pour before the pizza lands", "The day is built for lift and first impressions."),
        ("Ascending", "Charge"): ("Open as guests arrive", "Catch the aromatic spike before the room gets noisy."),
        ("Ascending", "Peak"): ("Prime time with the first slice", "This is the loudest version of the day."),
        ("Ascending", "Release"): ("Give it 15 minutes in glass", "The wine will bloom after a beat."),
        ("Descending", "Seed"): ("Taste after food hits the table", "Ground the palate before you judge the bottle."),
        ("Descending", "Charge"): ("Open, then wait 10 minutes", "A little air helps the structure come together."),
        ("Descending", "Peak"): ("Pour with something salty first", "The bottle wants an anchored landing."),
        ("Descending", "Release"): ("Save the first serious sip for the quiet moment", "This signal rewards patience."),
    }
    label, note = matrix[(state.motion, state.phase_arc)]
    return {"label": label, "note": note}


def decant_minutes(scores: dict[str, int], state: LunarState) -> int:
    if state.motion == "Descending" and scores["mineral"] >= 65:
        return 20
    if scores["texture"] >= 70:
        return 15
    if state.phase_arc == "Peak":
        return 5
    return 0


def build_table_plan(state: LunarState, scores: dict[str, int], party_mode: str, appetite: str) -> dict[str, Any]:
    decant = decant_minutes(scores, state)
    serve_cool = "Serve slightly cooler than room temp." if state.element in {"Fire", "Air"} else "Serve just under cellar temp."
    return {
        "pizza": PIZZA_PLAN[state.element][appetite],
        "wine": {
            **WINE_PLAN[state.element][appetite],
            "serve": serve_cool,
            "decant": "No decant needed." if decant == 0 else f"Give it about {decant} minutes of air.",
        },
        "side": SIDE_PLAN[state.element],
        "party_move": PARTY_MOVES[party_mode],
        "soundtrack": {
            "name": SOUNDTRACK[state.element]["base"],
            "note": SOUNDTRACK[state.element][state.phase_arc],
        },
        "ritual": RITUALS[(state.motion, state.phase_arc)],
    }


def axis_correction_note(profile: Mapping[str, Any], scores: Mapping[str, int], axis: str) -> str:
    if int(profile["traits"][axis]) < scores[axis]:
        return AXIS_UPSHIFT_NOTES[axis]
    return AXIS_DOWNSHIFT_NOTES[axis]


def service_temperature_note(profile: Mapping[str, Any]) -> str:
    if profile["key"] == DEFAULT_BOTTLE_PROFILE:
        return "Choose a bottle after you decide whether you want lift, herb, stone, or texture."

    if profile["key"] == CUSTOM_BOTTLE_PROFILE and profile["custom_config"]["sparkle"] != "still":
        return "Serve cold, open one beat before the food, and keep the pace brisk."

    if int(profile["traits"]["acid"]) >= 72:
        return "Start colder than usual and let the glass warm naturally."
    if int(profile["traits"]["texture"]) >= 70:
        return "Start near cellar temp and give the wine a bigger glass."
    return "Begin at cellar temp, then adjust on the second pour."


def build_service_map(
    selected_profile: Mapping[str, Any],
    scores: dict[str, int],
    fit: Mapping[str, Any],
    state: LunarState,
    appetite: str,
    party_mode: str,
) -> dict[str, Any]:
    if selected_profile["key"] == DEFAULT_BOTTLE_PROFILE:
        return {
            "title": "Signal-first shopping",
            "summary": "No bottle selected yet. Shop toward tonight's signal or build a custom bottle to get correction advice.",
            "items": [
                {
                    "label": "Shop for",
                    "title": ", ".join(item["name"] for item in top_profile_matches(scores, state, appetite, party_mode, count=2)),
                    "note": "These archetypes track the signal most closely tonight.",
                },
                {
                    "label": "Lead axis",
                    "title": dominant_axes(scores, count=1)[0]["label"],
                    "note": "If you're buying blind, chase the loudest axis of the night.",
                },
                {
                    "label": "Pour move",
                    "title": opening_window(state)["label"],
                    "note": opening_window(state)["note"],
                },
            ],
        }

    aligned_title = ", ".join(item["label"] for item in fit["aligned_axes"]) or "No clear alignment"
    tension_axis = fit["tension_axes"][0] if fit["tension_axes"] else None
    tension_title = tension_axis["label"] if tension_axis else "Minor tension"
    tension_note = (
        axis_correction_note(selected_profile, scores, tension_axis["key"])
        if tension_axis
        else "This bottle already sits close to the signal. Do not over-correct the food."
    )
    blueprint_title = selected_profile.get("style_line", selected_profile["name"]).capitalize()
    blueprint_note = selected_profile["note"]
    return {
        "title": f"{selected_profile['name']} service map",
        "summary": f"{selected_profile['name']} fits best when you lean into {aligned_title.lower()}.",
        "items": [
            {
                "label": "Blueprint",
                "title": blueprint_title,
                "note": blueprint_note,
            },
            {
                "label": "Lean into",
                "title": aligned_title,
                "note": "These axes already line up with the lunar signal. Let the pizza and service emphasize them.",
            },
            {
                "label": "Correct for",
                "title": tension_title,
                "note": tension_note,
            },
            {
                "label": "Pour move",
                "title": service_temperature_note(selected_profile),
                "note": opening_window(state)["note"],
            },
        ],
    }


def proof_claim(scores: dict[str, int]) -> str:
    top_axis = dominant_axes(scores, count=1)[0]["key"]
    if top_axis == "fruit":
        return "Believers would say fruit should outrun structure tonight."
    if top_axis == "floral":
        return "Believers would say the nose should arrive before the body."
    if top_axis == "herbal":
        return "Believers would say leafy, saline detail should show early."
    if top_axis == "mineral":
        return "Believers would say the bottle should feel tighter, stonier, and more architectural."
    if top_axis == "texture":
        return "Believers would say texture should matter more than aroma on this signal."
    return "Believers would say this is a high-energy pour that should read louder than usual."


def build_proof_lab(
    today: dict[str, Any],
    tomorrow: dict[str, Any],
    verdict: str,
    selected_profile: Mapping[str, Any],
) -> dict[str, Any]:
    if verdict == "Hold Until Tomorrow":
        compare_line = "Open a casual bottle tonight, then use the special one tomorrow and compare your notes."
    elif verdict == "Split the Difference":
        compare_line = "The signal barely moves overnight, which makes this a perfect test case for whether you feel the theory at all."
    else:
        compare_line = "Open the better bottle tonight, but save a splash for tomorrow if you want the comparison."

    if selected_profile["key"] != DEFAULT_BOTTLE_PROFILE:
        compare_line = f"{compare_line} Selected bottle: {selected_profile['name']}."

    return {
        "claim": proof_claim(today["scores"]),
        "compare_line": compare_line,
        "protocol": [
            "Take a first sip before the first bite and write three words.",
            "Take a second sip after two bites and score fruit, aroma, and savoriness from 1 to 5.",
            "Repeat tomorrow if you can with the same style of wine and see what actually changed.",
        ],
        "prompts": [
            "What arrived first: fruit, aroma, or structure?",
            "Did the pizza make the wine feel louder or tighter?",
            "Would you open a better bottle on this signal again?",
        ],
        "tomorrow_signal": tomorrow["signal_name"],
    }


def compare_reason(
    today: dict[str, Any],
    tomorrow: dict[str, Any],
    appetite: str,
    selected_profile: Mapping[str, Any],
) -> dict[str, Any]:
    using_profile = selected_profile["key"] != DEFAULT_BOTTLE_PROFILE
    metric_name = selected_profile["name"] if using_profile else "special bottle window"
    today_metric = today["profile_fit"]["score"] if using_profile else today["bottle_score"]
    tomorrow_metric = tomorrow["profile_fit"]["score"] if using_profile else tomorrow["bottle_score"]

    deltas = {
        key: tomorrow["scores"][key] - today["scores"][key]
        for key in ("fruit", "floral", "herbal", "mineral", "texture", "acid", "intensity")
    }
    ranked = sorted(deltas.items(), key=lambda item: abs(item[1]), reverse=True)
    top_changes = []
    for key, change in ranked[:2]:
        direction = "higher" if change > 0 else "lower"
        top_changes.append(f"{AXIS_LABELS[key]} is {direction} tomorrow")

    score_gap = round(today_metric - tomorrow_metric, 1)

    if abs(score_gap) <= 1.5:
        verdict = "Split the Difference"
        headline = "The signal barely moves overnight."
        summary = f"Treat this as a tasting experiment, not a hunt for fake precision. {', '.join(top_changes)}."
    elif tomorrow_metric > today_metric + 1.9:
        verdict = "Hold Until Tomorrow"
        headline = "Tomorrow carries the stronger window."
        summary = f"{metric_name} fits tomorrow better. Tonight is still usable, but {', '.join(top_changes)}."
    else:
        verdict = "Open Tonight"
        headline = "Tonight is the better pour."
        if using_profile:
            summary = f"{metric_name} lands better on tonight's signal for a {appetite} table."
        else:
            summary = f"The base signal already suits a {appetite} table, and {today['signal_name']} has the better opening score."

    return {
        "verdict": verdict,
        "headline": headline,
        "summary": summary,
        "delta": score_gap,
        "metric_name": metric_name,
    }


def serialize_forecast(
    day: date,
    party_mode: str,
    appetite: str,
    selected_profile: Mapping[str, Any],
) -> dict[str, Any]:
    state = build_lunar_state(day)
    scores = score_axes(state)
    forecast = {
        "date": day.isoformat(),
        "weekday": day.strftime("%A"),
        "moon_phase": state.moon_phase,
        "phase_arc": state.phase_arc,
        "zodiac_sign": state.zodiac_sign,
        "day_type": state.day_type,
        "element": state.element,
        "motion": state.motion,
        "signal_name": state.signal_name,
        "thesis": compose_thesis(state, scores),
        "scores": scores,
        "dominant_axes": dominant_axes(scores),
        "opening_window": opening_window(state),
        "palette": PALETTE_BY_ELEMENT[state.element],
    }
    forecast["table_plan"] = build_table_plan(state, scores, party_mode, appetite)
    forecast["bottle_score"] = bottle_score(scores, appetite, party_mode)
    forecast["profile_fit"] = profile_fit_detail(selected_profile, scores, state, appetite, party_mode)
    forecast["top_profiles"] = top_profile_matches(scores, state, appetite, party_mode)
    forecast["service_map"] = build_service_map(selected_profile, scores, forecast["profile_fit"], state, appetite, party_mode)
    return forecast


def build_week_horizon(
    requested_day: date,
    party_mode: str,
    appetite: str,
    selected_profile: Mapping[str, Any],
) -> dict[str, Any]:
    nights = []
    for offset in range(7):
        day = requested_day + timedelta(days=offset)
        forecast = serialize_forecast(day, party_mode, appetite, selected_profile)
        score = forecast["profile_fit"]["score"] if selected_profile["key"] != DEFAULT_BOTTLE_PROFILE else forecast["bottle_score"]
        top_profile = forecast["top_profiles"][0]
        nights.append(
            {
                "date": forecast["date"],
                "weekday": forecast["weekday"],
                "signal_name": forecast["signal_name"],
                "drinking_well": top_profile["name"],
                "drinking_well_note": top_profile["note"],
                "moon_phase": forecast["moon_phase"],
                "day_type": forecast["day_type"],
                "phase_arc": forecast["phase_arc"],
                "motion": forecast["motion"],
                "score": score,
                "top_axis": forecast["dominant_axes"][0]["label"],
            }
        )

    ranked = sorted(nights, key=lambda item: item["score"], reverse=True)
    best_date = ranked[0]["date"]
    second_best = ranked[1]["date"] if len(ranked) > 1 else None
    for item in nights:
        if item["date"] == best_date:
            item["status"] = "Best Night"
        elif second_best and item["date"] == second_best:
            item["status"] = "Strong Night"
        elif item["score"] <= ranked[-1]["score"] + 1:
            item["status"] = "Quiet Night"
        else:
            item["status"] = "Usable Night"

    return {"best_date": best_date, "nights": nights}


def build_cellar_strategy(
    week_horizon: dict[str, Any],
    selected_profile: Mapping[str, Any],
    today: dict[str, Any],
) -> dict[str, Any]:
    best_night = next(item for item in week_horizon["nights"] if item["date"] == week_horizon["best_date"])
    if selected_profile["key"] != DEFAULT_BOTTLE_PROFILE:
        if best_night["date"] == today["date"]:
            advice = f"{selected_profile['name']} is already in its best seven-night window."
        else:
            advice = f"If you want the clearest expression of {selected_profile['name']}, the strongest window is {best_night['weekday']}."
        return {
            "mode": "selected_profile",
            "title": selected_profile["name"],
            "advice": advice,
            "best_night": best_night,
            "style_line": selected_profile.get("style_line", selected_profile["name"]),
        }

    return {
        "mode": "archetype",
        "title": "Tonight's best archetypes",
        "advice": "If you have options in the cellar, these bottle shapes fit tonight best.",
        "best_night": best_night,
        "alternatives": today["top_profiles"],
    }


def build_experience(
    requested_day: date,
    party_mode: str,
    appetite: str,
    bottle_profile_key: str = DEFAULT_BOTTLE_PROFILE,
    custom_bottle: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_profile = resolve_selected_profile(bottle_profile_key, custom_bottle)
    normalized_custom = resolved_profile.get("custom_config", normalize_custom_bottle(custom_bottle))

    today = serialize_forecast(requested_day, party_mode, appetite, resolved_profile)
    tomorrow = serialize_forecast(requested_day + timedelta(days=1), party_mode, appetite, resolved_profile)
    decision = compare_reason(today, tomorrow, appetite, resolved_profile)
    proof_lab = build_proof_lab(today, tomorrow, decision["verdict"], resolved_profile)
    week_horizon = build_week_horizon(requested_day, party_mode, appetite, resolved_profile)
    cellar_strategy = build_cellar_strategy(week_horizon, resolved_profile, today)

    return {
        "requested_date": requested_day.isoformat(),
        "party_mode": party_mode,
        "appetite": appetite,
        "bottle_profile": bottle_profile_key,
        "custom_bottle": normalized_custom,
        "selected_bottle_profile": {
            "key": resolved_profile["key"],
            "name": resolved_profile["name"],
            "note": resolved_profile["note"],
            "style_line": resolved_profile.get("style_line", resolved_profile["name"]),
            "traits": resolved_profile.get("traits", {}),
            "affinities": resolved_profile.get("affinities", []),
        },
        "available_bottle_profiles": [
            {"key": key, "name": value["name"], "note": value["note"]}
            for key, value in BOTTLE_PROFILES.items()
        ],
        "generated_at": datetime.now(tz=LOS_ANGELES).isoformat(),
        "decision": decision,
        "today": today,
        "tomorrow": tomorrow,
        "proof_lab": proof_lab,
        "week_horizon": week_horizon,
        "cellar_strategy": cellar_strategy,
    }
