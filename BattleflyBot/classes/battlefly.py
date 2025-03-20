import json
from dataclasses import dataclass
from typing import List

# Load type data from JSON
try:
    with open("data/battlefly_types.json", "r") as f:
        TYPE_DATA = json.load(f)
except FileNotFoundError:
    TYPE_DATA = {}
    print("⚠️ Warning: battlefly_types.json not found. Battlefly types will not load correctly.")

@dataclass
class Battlefly:
    name: str
    img_path: str
    rarity: str  # Common, Uncommon, Rare, Epic, Legendary
    stage: str  # Egg, Caterpillar, Battlefly
    type: str  # Firefly, Leaffly, Stonefly, Stormfly, Icefly, Venomfly, Glowfly
    attack_trait: str
    strengths: List[str]
    weaknesses: List[str]

    def __init__(self, name, img_path, rarity, stage, type):
        self.name = name
        self.img_path = img_path
        self.rarity = rarity
        self.stage = stage
        self.type = type
        
        # Get type-specific data from JSON
        type_data = TYPE_DATA.get(type, {})
        self.attack_trait = type_data.get("attack_trait", "Unknown")
        self.strengths = type_data.get("strengths", [])
        self.weaknesses = type_data.get("weaknesses", [])
