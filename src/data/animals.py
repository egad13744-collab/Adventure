import random
from typing import Dict, Any
from data.items import Rarity
},
    "dark_hydra": {
        "name": "Dark Hydra",
        "emoji_key": "dark_hydra",
        "hp": 90,
        "attack": 24,
        "defense": 18,
        "skill": {"name": "Multi-Head Strike", "type": "active", "effect": "Attacks 2-3 times per turn"},
        "rarity": Rarity.EPIC
    },
    "celestial_griffin": {
        "name": "Celestial Griffin",
        "emoji_key": "celestial_griffin",
        "hp": 100,
        "attack": 35,
        "defense": 20,
        "skill": {"name": "Divine Wings", "type": "passive", "effect": "+25% damage and defense"},
        "rarity": Rarity.LEGENDARY
    },
    "ancient_dragon": {
        "name": "Ancient Dragon",
        "emoji_key": "ancient_dragon",
        "hp": 120,
        "attack": 40,
        "defense": 25,
        "skill": {"name": "Dragon Rage", "type": "active", "effect": "Deals massive damage, increases each turn"},
        "rarity": Rarity.LEGENDARY
    },
    "void_serpent": {
        "name": "Void Serpent",
        "emoji_key": "void_serpent",
        "hp": 150,
        "attack": 50,
        "defense": 30,
        "skill": {"name": "Void Consume", "type": "active", "effect": "Absorbs 30% of damage dealt as HP"},
        "rarity": Rarity.MYTHIC
    },
    "cosmic_phoenix": {
        "name": "Cosmic Phoenix",
        "emoji_key": "cosmic_phoenix",
        "hp": 130,
        "attack": 55,
        "defense": 25,
        "skill": {"name": "Eternal Flame", "type": "passive", "effect": "Cannot be one-shot, revives twice"},
        "rarity": Rarity.MYTHIC
    },
    "prism_butterfly": {
        "name": "Prism Butterfly",
        "emoji_key": "prism_butterfly",
        "hp": 180,
        "attack": 65,
        "defense": 35,
        "skill": {"name": "Rainbow Shield", "type": "passive", "effect": "50% chance to nullify damage"},
        "rarity": Rarity.EXOTIC
    },
    "eternal_sphinx": {
        "name": "Eternal Sphinx",
        "emoji_key": "eternal_sphinx",
        "hp": 200,
        "attack": 70,
        "defense": 40,
        "skill": {"name": "Riddle of Ages", "type": "active", "effect": "Confuses enemy, 40% miss chance"},
        "rarity": Rarity.EXOTIC
    },
    "chrono_serpent": {
        "name": "Chrono Serpent",
        "emoji_key": "chrono_serpent",
        "hp": 190,
        "attack": 68,
        "defense": 38,
        "skill": {"name": "Time Rewind", "type": "active", "effect": "Reverts last attack, heals 25% HP"},
        "rarity": Rarity.EXOTIC
    },
    "nebula_wolf": {
        "name": "Nebula Wolf",
        "emoji_key": "nebula_wolf",
        "hp": 175,
        "attack": 72,
        "defense": 36,
        "skill": {"name": "Starfall Howl", "type": "active", "effect": "Hits all enemies for 50% damage"},
        "rarity": Rarity.EXOTIC
    },
    "jade_emperor": {
        "name": "Jade Emperor",
        "emoji_key": "jade_emperor",
        "hp": 210,
        "attack": 66,
        "defense": 45,
        "skill": {"name": "Imperial Decree", "type": "passive", "effect": "+30% defense, immune to stun"},
        "rarity": Rarity.EXOTIC
    },
    "starlight_angel": {
        "name": "Starlight Angel",
        "emoji_key": "starlight_angel",
        "hp": 250,
        "attack": 80,
        "defense": 50,
        "skill": {"name": "Divine Blessing", "type": "passive", "effect": "Heals all team 10% per turn"},
        "rarity": Rarity.CELESTIAL
    },
    "galaxy_titan": {
        "name": "Galaxy Titan",
        "emoji_key": "galaxy_titan",
        "hp": 300,
        "attack": 90,
        "defense": 60,
        "skill": {"name": "Cosmic Slam", "type": "active", "effect": "Deals 2x damage, stuns for 2 turns"},
        "rarity": Rarity.CELESTIAL
    },
    "lunar_empress": {
        "name": "Lunar Empress",
        "emoji_key": "lunar_empress",
        "hp": 270,
        "attack": 85,
        "defense": 55,
        "skill": {"name": "Moonlight Veil", "type": "passive", "effect": "60% chance to dodge attacks at night"},
        "rarity": Rarity.CELESTIAL
    },
    "solar_guardian": {
        "name": "Solar Guardian",
        "emoji_key": "solar_guardian",
        "hp": 280,
        "attack": 95,
        "defense": 52,
        "skill": {"name": "Solar Flare", "type": "active", "effect": "Burns all enemies, +20% damage for 3 turns"},
        "rarity": Rarity.CELESTIAL
    },
    "aurora_phoenix": {
        "name": "Aurora Phoenix",
        "emoji_key": "aurora_phoenix",
        "hp": 260,
        "attack": 88,
        "defense": 58,
        "skill": {"name": "Eternal Dawn", "type": "passive", "effect": "Revives with 50% HP, heals team 20%"},
        "rarity": Rarity.CELESTIAL
    },
    "shadow_king": {
        "name": "Shadow King",
        "emoji_key": "shadow_king",
        "hp": 400,
        "attack": 120,
        "defense": 80,
        "skill": {"name": "Absolute Darkness", "type": "passive", "effect": "Immune to all debuffs, +50% all stats"},
        "rarity": Rarity.SECRET
    },
    "world_serpent": {
        "name": "World Serpent",
        "emoji_key": "world_serpent",
        "hp": 450,
        "attack": 110,
        "defense": 85,
        "skill": {"name": "Ragnarok Coil", "type": "active", "effect": "Deals 3x damage, poisons for 5 turns"},
        "rarity": Rarity.SECRET
    },
    "genesis_dragon": {
        "name": "Genesis Dragon",
        "emoji_key": "genesis_dragon",
        "hp": 500,
        "attack": 130,
        "defense": 75,
        "skill": {"name": "Creation Breath", "type": "passive", "effect": "Summons ally with 30% stats each turn"},
        "rarity": Rarity.SECRET
    },
    "time_weaver": {
        "name": "Time Weaver",
        "emoji_key": "time_weaver",
        "hp": 380,
        "attack": 115,
        "defense": 90,
        "skill": {"name": "Temporal Loop", "type": "active", "effect": "Attacks twice, enemy skips next turn"},
        "rarity": Rarity.SECRET
    },
    "primordial_beast": {
        "name": "Primordial Beast",
        "emoji_key": "primordial_beast",
        "hp": 550,
        "attack": 140,
        "defense": 70,
        "skill": {"name": "Extinction Wave", "type": "active", "effect": "Instantly defeats enemies below 30% HP"},
        "rarity": Rarity.SECRET
    }
}

WILD_MONSTERS: Dict[str, Dict[str, Any]] = {
    "slime": {
        "name": "Wild Slime",
        "emoji": "🟢",
        "hp": 30,
        "attack": 5,
        "defense": 2,
        "exp_reward": 15,
        "coin_reward": (5, 15),
        "rarity": Rarity.COMMON
    },
    "goblin": {
        "name": "Goblin Scout",
        "emoji": "👺",
        "hp": 45,
        "attack": 10,
        "defense": 5,
        "exp_reward": 25,
        "coin_reward": (10, 30),
        "rarity": Rarity.COMMON
    },
    "skeleton": {
        "name": "Skeleton Warrior",
        "emoji": "💀",
        "hp": 60,
        "attack": 15,
        "defense": 8,
        "exp_reward": 40,
        "coin_reward": (20, 50),
        "rarity": Rarity.UNCOMMON
    },
    "orc": {
        "name": "Orc Brute",
        "emoji": "👹",
        "hp": 80,
        "attack": 20,
        "defense": 12,
        "exp_reward": 60,
        "coin_reward": (30, 70),
        "rarity": Rarity.UNCOMMON
    },
    "dark_knight": {
        "name": "Dark Knight",
        "emoji": "🗡️",
        "hp": 100,
        "attack": 28,
        "defense": 18,
        "exp_reward": 100,
        "coin_reward": (50, 120),
        "rarity": Rarity.RARE
    },
    "demon": {
        "name": "Lesser Demon",
        "emoji": "😈",
        "hp": 130,
        "attack": 35,
        "defense": 20,
        "exp_reward": 150,
        "coin_reward": (80, 180),
        "rarity": Rarity.RARE
    },
    "dragon_whelp": {
        "name": "Dragon Whelp",
        "emoji": "🐲",
        "hp": 180,
        "attack": 45,
        "defense": 28,
        "exp_reward": 250,
        "coin_reward": (150, 300),
        "rarity": Rarity.EPIC
    },
    "demon_lord": {
        "name": "Demon Lord",
        "emoji": "👿",
        "hp": 250,
        "attack": 55,
        "defense": 35,
        "exp_reward": 400,
        "coin_reward": (250, 500),
        "rarity": Rarity.EPIC
    },
    "elder_dragon": {
        "name": "Elder Dragon",
        "emoji": "🐉",
        "hp": 400,
        "attack": 70,
        "defense": 45,
        "exp_reward": 700,
        "coin_reward": (500, 1000),
        "rarity": Rarity.LEGENDARY
    },
    "void_titan": {
        "name": "Void Titan",
        "emoji": "🌀",
        "hp": 600,
        "attack": 90,
        "defense": 55,
        "exp_reward": 1200,
        "coin_reward": (1000, 2000),
        "rarity": Rarity.MYTHIC
    }
}

def get_random_animal(luck_bonus: int = 0) -> Dict[str, Any]:
    weights = []
    animals = list(ANIMALS.items())
    
    for animal_id, animal in animals:
        base_weight = animal["rarity"].drop_chance
        if luck_bonus > 0 and animal["rarity"] in [Rarity.RARE, Rarity.EPIC, Rarity.LEGENDARY, Rarity.MYTHIC, Rarity.EXOTIC, Rarity.CELESTIAL, Rarity.SECRET]:
            base_weight += luck_bonus * 0.15
        weights.append(base_weight)
    
    selected_id, selected = random.choices(animals, weights=weights, k=1)[0]
    result = selected.copy()
    result['animal_id'] = selected_id
    return result

def get_random_monster(luck_bonus: int = 0) -> Dict[str, Any]:
    weights = []
    monsters = list(WILD_MONSTERS.items())
    
    for monster_id, monster in monsters:
        base_weight = monster["rarity"].drop_chance
        if luck_bonus > 0 and monster["rarity"] in [Rarity.RARE, Rarity.EPIC, Rarity.LEGENDARY, Rarity.MYTHIC]:
            base_weight += luck_bonus * 0.1
        weights.append(base_weight)
    
    selected_id, selected = random.choices(monsters, weights=weights, k=1)[0]
    result = selected.copy()
    result['monster_id'] = selected_id
    return result

def get_animal_by_id(animal_id: str) -> Dict[str, Any]:
    if animal_id in ANIMALS:
        result = ANIMALS[animal_id].copy()
        result['animal_id'] = animal_id
        return result
    return None
