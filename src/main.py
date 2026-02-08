import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from database.db import Database

intents = discord.Intents.default()
intents.message_content = True

class AdventureBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="q", intents=intents, help_command=None)
        self.db = Database()
        
    async def setup_hook(self):
        await self.db.init()
        
        cogs = [
            'cogs.profile',
            'cogs.hunt',
            'cogs.fish',
            'cogs.inventory',
            'cogs.shop',
            'cogs.daily',
            'cogs.minigames',
            'cogs.battle',
            'cogs.trade',
            'cogs.animal',
            'cogs.leaderboard',
            'cogs.prestige',
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"Loaded {cog}")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")
        
        await self.tree.sync()
        print("Slash commands synced!")
        
    async def on_ready(self):
        print(f'{self.user} is now online!')
        print(f'Connected to {len(self.guilds)} servers')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="/help atau qhelp | Adventure Quest"
            )
        )

bot = AdventureBot()

@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    embed = create_help_embed()
    await interaction.response.send_message(embed=embed)

@bot.command(name="help")
async def help_prefix(ctx):
    embed = create_help_embed()
    await ctx.send(embed=embed)

def create_help_embed():
    embed = discord.Embed(
        title="Adventure Quest - Commands",
        description="Selamat datang di Adventure Quest!\n"
                    "**Slash Command:** `/command`\n"
                    "**Prefix Command:** `qcommand`",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="👤 Profil & Stats",
        value="`/profile` `qprofile` - Lihat profilmu\n"
              "`/inventory` `qinventory` - Cek itemmu\n"
              "`/daily` `qdaily` - Hadiah harian",
        inline=False
    )
    
    embed.add_field(
        name="🏹 Berburu & Hewan",
        value="`/hunt` `qhunt` - Tangkap hewan\n"
              "`/animal list` `qanimal list` - Lihat hewanmu\n"
              "`/animal equip` `qanimal equip` - Tambah ke tim\n"
              "`/animal unequip` - Keluarkan dari tim\n"
              "`/animal heal` `qanimal heal` - Sembuhkan tim\n"
              "`/team` `qteam` - Lihat tim battle",
        inline=False
    )
    
    embed.add_field(
        name="⚔️ Battle",
        value="`/battle` `qbattle` - Lawan monster\n"
              "*Wajib punya hewan di tim!*",
        inline=False
    )
    
    embed.add_field(
        name="🎣 Memancing",
        value="`/fish` `qfish` - Memancing item",
        inline=False
    )
    
    embed.add_field(
        name="💰 Ekonomi",
        value="`/shop` `qshop` - Lihat toko\n"
              "`/buy` `qbuy` - Beli item\n"
              "`/sell` `qsell` - Jual item\n"
              "`/sell animal <rarity>` - Jual hewan massal\n"
              "  Kode: C/U/R/E/L/M/X/CE/S",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Mini Games",
        value="`/guess` `qguess` - Tebak angka\n"
              "`/slots` `qslots` - Mesin slot",
        inline=False
    )
    
    embed.add_field(
        name="🏆 Leaderboard",
        value="`/leaderboard` `qleaderboard` - Peringkat\n"
              "`/leaderboard coin` - Top koin\n"
              "`/leaderboard level` - Top level\n"
              "`/leaderboard win` - Top win",
        inline=False
    )
    
    embed.set_footer(text="Adventure Quest | Cooldown: 10 detik")
    return embed

if __name__ == "__main__":
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: DISCORD_BOT_TOKEN not found in environment variables!")
        print("Please set your Discord bot token.")
    else:
        bot.run(token)
