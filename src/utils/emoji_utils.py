from data.emoji_map import EMOJI_MAP
from data.animals import get_animal_by_id

def get_animal_emoji(animal_id: str, costume: str = None) -> str:
    animal_data = get_animal_by_id(animal_id)
    if not animal_data:
        return EMOJI_MAP.get("default", "🐾")
    
    # Check if costume exists and has a mapping
    if costume and "costumes" in animal_data and costume in animal_data["costumes"]:
        emoji_key = animal_data["costumes"][costume]
    else:
        emoji_key = animal_data.get("emoji_key")
        
    return EMOJI_MAP.get(emoji_key, EMOJI_MAP.get("default", "🐾"))
