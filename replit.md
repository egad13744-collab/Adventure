# Adventure Quest Discord Bot

## Overview
A Discord RPG + Economy bot inspired by OwO Bot but with completely original systems, names, and mechanics. Features hunting to capture animals, animal-based battle system, fishing, mini-games, and a full economy system.

## Project Structure
```
src/
├── main.py           # Bot entry point and help command
├── database/
│   ├── __init__.py
│   └── db.py         # PostgreSQL database handler (users, animals, inventory)
├── data/
│   ├── __init__.py
│   ├── items.py      # Items, weapons, rods, skins with rarity
│   ├── monsters.py   # Legacy monster definitions
│   └── animals.py    # Animal & wild monster definitions for battle
└── cogs/
    ├── __init__.py
    ├── profile.py    # /profile, /equip, /unequip
    ├── hunt.py       # /hunt - capture animals
    ├── fish.py       # /fish command
    ├── inventory.py  # /inventory command
    ├── shop.py       # /shop, /buy, /sell (item & animal)
    ├── daily.py      # /daily reward
    ├── minigames.py  # /guess, /slots
    ├── battle.py     # /battle - PvE with animal team
    ├── animal.py     # /animal list/equip/unequip/info/heal, /team
    ├── leaderboard.py # /leaderboard coin/level/win
    └── trade.py      # /trade, /accept_trade, /decline_trade
```

## Recent Changes (Feb 2, 2026)

### Dual Command Support
- Slash commands: `/command`
- Prefix commands: `qcommand`
- Both use the same logic (no duplication)

### Cooldown System (10 seconds)
- Battle: 10 seconds
- Hunt: 10 seconds
- Fish: 10 seconds
- Gambling (slots/guess): 10 seconds

### Pagination for Animal List
- 10 animals per page
- Navigation buttons (Prev/Next)
- Shows: ID, Name, Rarity (with code), Level, Status

### Mass Sell Animals by Rarity
- `/sell animal <rarity_code>` or `qsell animal <code>`
- Rarity codes: C, U, R, E, L, M, X, CE, S
- Animals in team protected (cannot be sold)

### Updated Rarity System (9 levels)
| Rarity | Code | Drop Rate | Sell Price |
|--------|------|-----------|------------|
| Common | C | 50% | 10 |
| Uncommon | U | 20% | 25 |
| Rare | R | 15% | 75 |
| Epic | E | 3% | 200 |
| Legendary | L | 1% | 500 |
| Mythic | M | 0.5% | 1,500 |
| Exotic | X | 0.1% | 5,000 |
| Celestial | CE | 0.05% | 15,000 |
| Secret | S | 0.01% | 50,000 |

## Core Game Mechanics

### Hunt System
- `/hunt` or `qhunt` captures wild **animals**
- Each animal has: Name, Rarity, HP, Attack, Defense, Skill
- Animals automatically added to Animal Inventory
- Cooldown: 10 seconds

### Animal System
- **Animal Inventory**: Store all captured animals
- **Animal Team**: Max 3 animals for battle (unlocks based on player level)
- Commands (slash & prefix):
  - `/animal list` `qanimal list` - View all animals (paginated)
  - `/animal equip` `qanimal equip` - Add to team
  - `/animal unequip` - Remove from team
  - `/animal info` `qanimal info` - Detailed animal info
  - `/animal heal` `qanimal heal` - Heal team (costs coins)
  - `/team` `qteam` - View battle team

### Battle System
- **Battle ALWAYS uses Animal Team**
- Cannot battle without at least 1 animal in team
- Turn-based combat with animals fighting
- Animals gain EXP from battle and can level up
- Player acts as commander (gives bonuses via equipment)
- Cooldown: 10 seconds

### Animal Skills
Each animal has a skill (passive or active):
- **Passive**: Always active (e.g., +10% attack)
- **Active**: Triggers during battle (e.g., life drain, stun)

### Progression
- Animals gain EXP from battles
- Animals level up and get stat boosts
- Player level unlocks more team slots

### Balance Rules
- Battle requires animals - no battle without team
- Equipment gives small bonuses only
- Not pay-to-win

## Commands
| Command | Prefix | Description |
|---------|--------|-------------|
| `/help` | `qhelp` | Show all commands |
| `/profile` | `qprofile` | View your profile |
| `/inventory` | `qinventory` | View your items |
| `/equip` | `qequip` | Equip player equipment |
| `/unequip` | `qunequip` | Unequip player equipment |
| `/hunt` | `qhunt` | Hunt to capture animals |
| `/fish` | `qfish` | Go fishing for items |
| `/animal list` | `qanimal list` | View all your animals |
| `/animal equip` | `qanimal equip` | Add animal to team |
| `/animal unequip` | - | Remove animal from team |
| `/animal info` | `qanimal info` | View animal details |
| `/animal heal` | `qanimal heal` | Heal all team animals |
| `/team` | `qteam` | View battle team |
| `/battle` | `qbattle` | Fight monsters with your team |
| `/daily` | `qdaily` | Claim daily reward |
| `/shop` | `qshop` | Browse shop |
| `/buy` | `qbuy` | Buy an item |
| `/sell item` | `qsell item` | Sell items |
| `/sell animal` | `qsell animal` | Sell animals by rarity |
| `/guess` | `qguess` | Number guessing game |
| `/slots` | `qslots` | Slot machine |
| `/leaderboard` | `qleaderboard` | View leaderboard |

## Technical Details
- Language: Python 3.11
- Framework: discord.py
- Database: PostgreSQL (Replit built-in)
- Commands: Slash commands (/) & Prefix commands (q)
- Architecture: Modular cogs system

## Database Tables
- `users` - Player profiles (with last_battle, last_gamble cooldowns)
- `inventory` - Item storage
- `animals` - Captured animals with stats
- `battle_stats` - Win/loss tracking
- `trades` - Trade records

## Environment Variables Required
- `DISCORD_BOT_TOKEN` - Your Discord bot token

## Running the Bot
The bot runs via `python src/main.py`

## User Preferences
- Response language: Bahasa Indonesia
