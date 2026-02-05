import discord
from discord import app_commands
from discord.ext import commands
from data.animals import get_animal_by_id, ANIMALS
from data.items import Rarity, get_rarity_by_code, RARITY_SELL_PRICES
from utils.emoji_utils import get_animal_emoji
import math

ANIMALS_PER_PAGE = 10

class AnimalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    animal_group = app_commands.Group(name="animal", description="Manage your animals")
    
async def do_animal_list(self, user_id: int, username: str, page: int = 1):
    await self.db.get_user(user_id, username)
    animals = await self.db.get_user_animals(user_id)

    if not animals:
        embed = discord.Embed(
            title="🐾 Koleksi Hewanmu",
            description="Kamu belum punya hewan!\nGunakan `/hunt` atau `qhunt` untuk menangkap hewan pertamamu.",
            color=discord.Color.orange()
        )
        return embed, 0, 0

    total_pages = math.ceil(len(animals) / ANIMALS_PER_PAGE)
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * ANIMALS_PER_PAGE
    end_idx = start_idx + ANIMALS_PER_PAGE
    page_animals = animals[start_idx:end_idx]

    embed = discord.Embed(
        title=f"🐾 Koleksi Hewan {username}",
        description=f"Total: **{len(animals)}** hewan | Halaman **{page}/{total_pages}**",
        color=discord.Color.blue()
    )

    animal_list = ""
    for a in page_animals:
        emoji = get_animal_emoji(a['animal_id'], a.get('costume'))
        animal_data = get_animal_by_id(a['animal_id'])
        if animal_data:
            rarity = animal_data['rarity'].display_name
            rarity_code = animal_data['rarity'].short_code
            animal_name = animal_data['name']
        else:
            rarity = "Unknown"
            rarity_code = "?"
            animal_name = "Unknown"

        status = "⚔️ Tim" if a['is_in_team'] else "📦"
        animal_list += f"{emoji} **{a['nickname']}** ({animal_name}) | Lv.{a['level']} | {rarity} ({rarity_code}) | {status}\n"
        animal_list += f"   🆔 `{a['id']}` | ❤️ {a['current_hp']}/{a['max_hp']} | ⚔️ {a['attack']} | 🛡️ {a['defense']}\n"

    embed.add_field(
        name="📋 Daftar Hewan",
        value=animal_list if animal_list else "Kosong",
        inline=False
    )

    max_team = await self.db.get_max_team_size(user_id)
    team_count = len([a for a in animals if a['is_in_team']])
    embed.set_footer(text=f"Tim: {team_count}/{max_team} | /animal list <page> untuk halaman lain")

    return embed, page, total_pages


@commands.command(name="animal")
async def animal_prefix(self, ctx, subcommand: str = None, arg: str = None):
    if subcommand is None or subcommand.lower() == "list":
        page = 1
        if arg and arg.isdigit():
            page = int(arg)
        embed, current_page, total_pages = await self.do_animal_list(
            ctx.author.id, ctx.author.display_name, page
        )
        if total_pages > 1:
            view = AnimalListView(self, ctx.author.id, ctx.author.display_name, current_page, total_pages)
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(embed=embed)

    elif subcommand.lower() == "equip" and arg:
        success, message = await self.do_animal_equip(ctx.author.id, arg)
        await ctx.send(message)

    elif subcommand.lower() == "unequip" and arg:
        success, message = await self.do_animal_unequip(ctx.author.id, arg)
        await ctx.send(message)

    elif subcommand.lower() == "info" and arg:
        embed = await self.do_animal_info(ctx.author.id, arg)
        await ctx.send(embed=embed)

    elif subcommand.lower() == "heal":
        embed = await self.do_animal_heal(ctx.author.id, ctx.author.name)
        await ctx.send(embed=embed)

    else:
        await ctx.send("❌ Penggunaan: `qanimal list/equip/unequip/info/heal <id>`")
    
    async def do_animal_equip(self, user_id: int, animal_id: str):
        animal = await self.db.get_animal(animal_id)
        
        if not animal or animal['user_id'] != user_id:
            return False, "❌ Hewan tidak ditemukan atau bukan milikmu!"
        
        if animal['is_in_team']:
            return False, "❌ Hewan ini sudah ada di timmu!"
        
        success = await self.db.add_animal_to_team(user_id, animal_id)
        
        if not success:
            max_team = await self.db.get_max_team_size(user_id)
            return False, f"❌ Tim sudah penuh! (Maksimal {max_team} hewan)\nGunakan `/animal unequip <id>` untuk mengeluarkan hewan dari tim."
        
        animal_data = get_animal_by_id(animal['animal_id'])
        emoji = get_animal_emoji(animal['animal_id'], animal.get('costume'))
        
        return True, f"✅ {emoji} **{animal['nickname']}** (Lv.{animal['level']}) ditambahkan ke tim!"
    
    @animal_group.command(name="equip", description="Add an animal to your battle team")
    @app_commands.describe(animal_id="The ID of the animal to add to your team")
    async def animal_equip(self, interaction: discord.Interaction, animal_id: str):
        await self.db.get_user(interaction.user.id, interaction.user.name)
        success, message = await self.do_animal_equip(interaction.user.id, animal_id)
        await interaction.response.send_message(message, ephemeral=not success)
    
    async def do_animal_unequip(self, user_id: int, animal_id: str):
        animal = await self.db.get_animal(animal_id)
        
        if not animal or animal['user_id'] != user_id:
            return False, "❌ Hewan tidak ditemukan atau bukan milikmu!"
        
        if not animal['is_in_team']:
            return False, "❌ Hewan ini tidak ada di timmu!"
        
        await self.db.remove_animal_from_team(user_id, animal_id)
        
        emoji = get_animal_emoji(animal['animal_id'], animal.get('costume'))
        
        return True, f"✅ {emoji} **{animal['nickname']}** telah dipindahkan ke cadangan."
    
    @animal_group.command(name="unequip", description="Remove an animal from your battle team")
    @app_commands.describe(animal_id="The ID of the animal to remove from your team")
    async def animal_unequip(self, interaction: discord.Interaction, animal_id: str):
        success, message = await self.do_animal_unequip(interaction.user.id, animal_id)
        await interaction.response.send_message(message, ephemeral=not success)
    
    async def do_animal_info(self, user_id: int, animal_id: str):
        animal = await self.db.get_animal(animal_id)
        
        if not animal or animal['user_id'] != user_id:
            return discord.Embed(title="❌ Error", description="Hewan tidak ditemukan atau bukan milikmu!", color=discord.Color.red())
        
        animal_data = get_animal_by_id(animal['animal_id'])
        if not animal_data:
            return discord.Embed(title="❌ Error", description="Data hewan tidak ditemukan!", color=discord.Color.red())
        
        exp_needed = self.db.animal_exp_for_level(animal['level'])
        progress = int((animal['exp'] / exp_needed) * 10)
        progress_bar = "█" * progress + "░" * (10 - progress)
        
        emoji = get_animal_emoji(animal['animal_id'], animal.get('costume'))
        embed = discord.Embed(
            title=f"{emoji} {animal['nickname']}",
            description=f"**{animal_data['name']}** ({animal_data['rarity'].display_name} - {animal_data['rarity'].short_code})",
            color=animal_data['rarity'].color
        )
        
        embed.add_field(
            name="📊 Level",
            value=f"Level **{animal['level']}**\n"
                  f"EXP: {animal['exp']}/{exp_needed}\n"
                  f"[{progress_bar}]",
            inline=True
        )
        
        embed.add_field(
            name="⚔️ Stats",
            value=f"❤️ HP: {animal['current_hp']}/{animal['max_hp']}\n"
                  f"⚔️ Attack: {animal['attack']}\n"
                  f"🛡️ Defense: {animal['defense']}",
            inline=True
        )
        
        embed.add_field(
            name=f"✨ Skill: {animal_data['skill']['name']}",
            value=f"*{animal_data['skill']['effect']}*\n"
                  f"Type: {animal_data['skill']['type'].title()}",
            inline=False
        )
        
        status = "⚔️ Dalam Tim" if animal['is_in_team'] else "📦 Cadangan"
        embed.add_field(name="📍 Status", value=status, inline=True)
        embed.add_field(name="🆔 ID", value=f"`{animal['id']}`", inline=True)
        
        return embed
    
    @animal_group.command(name="info", description="View detailed info about an animal")
    @app_commands.describe(animal_id="The ID of the animal")
    async def animal_info(self, interaction: discord.Interaction, animal_id: str):
        embed = await self.do_animal_info(interaction.user.id, animal_id)
        await interaction.response.send_message(embed=embed)
    
    async def do_animal_heal(self, user_id: int, username: str):
        user = await self.db.get_user(user_id, username)
        
        team = await self.db.get_animal_team(user_id)
        
        if not team:
            return discord.Embed(title="❌ Error", description="Kamu tidak punya hewan di tim!", color=discord.Color.red())
        
        injured = [a for a in team if a['current_hp'] < a['max_hp']]
        
        if not injured:
            return discord.Embed(title="✅ Sehat", description="Semua hewanmu sudah sehat!", color=discord.Color.green())
        
        heal_cost = len(injured) * 20
        
        if user['coins'] < heal_cost:
            embed = discord.Embed(
                title="❌ Koin Tidak Cukup",
                description=f"Kamu butuh **{heal_cost}** koin untuk menyembuhkan timmu!\n"
                           f"Kamu hanya punya **{user['coins']}** koin.",
                color=discord.Color.red()
            )
            return embed
        
        await self.db.add_coins(user_id, -heal_cost)
        await self.db.heal_team(user_id)
        
        embed = discord.Embed(
            title="💚 Tim Disembuhkan!",
            description=f"Semua hewanmu telah disembuhkan!\n\n"
                        f"💰 Biaya: **{heal_cost}** koin",
            color=discord.Color.green()
        )
        
        return embed
    
    @animal_group.command(name="heal", description="Heal all animals in your team (costs coins)")
    async def animal_heal(self, interaction: discord.Interaction):
        embed = await self.do_animal_heal(interaction.user.id, interaction.user.name)
        await interaction.response.send_message(embed=embed)
    
    async def do_team_view(self, user_id: int, username: str):
        await self.db.get_user(user_id, username)
        
        team = await self.db.get_animal_team(user_id)
        max_team = await self.db.get_max_team_size(user_id)
        
        embed = discord.Embed(
            title=f"⚔️ Tim Battle {username}",
            color=discord.Color.gold()
        )
        
        if not team:
            embed.description = (
                "❌ **Tim Kosong!**\n\n"
                "Kamu tidak bisa battle tanpa hewan!\n"
                "1. Gunakan `/hunt` atau `qhunt` untuk menangkap hewan\n"
                "2. Gunakan `/animal equip <id>` untuk menambahkan ke tim"
            )
        else:
            for a in sorted(team, key=lambda x: x['team_slot'] or 0):
                animal_data = get_animal_by_id(a['animal_id'])
                emoji = get_animal_emoji(a['animal_id'], a.get('costume'))
                rarity = animal_data['rarity'].display_name if animal_data else "Unknown"
                skill_name = animal_data['skill']['name'] if animal_data else "Unknown"
                
                hp_percent = (a['current_hp'] / a['max_hp']) * 100
                hp_bar_len = int(hp_percent / 10)
                hp_bar = "🟩" * hp_bar_len + "🟥" * (10 - hp_bar_len)
                
                embed.add_field(
                    name=f"Slot {a['team_slot']}: {emoji} {a['nickname']} (Lv.{a['level']})",
                    value=f"**{rarity}**\n"
                          f"❤️ {a['current_hp']}/{a['max_hp']} {hp_bar}\n"
                          f"⚔️ ATK: {a['attack']} | 🛡️ DEF: {a['defense']}\n"
                          f"✨ {skill_name}",
                    inline=False
                )
            
            embed.description = f"Tim siap untuk battle! ({len(team)}/{max_team} slot)"
        
        embed.set_footer(text=f"Max Team Size: {max_team} | Level up untuk unlock lebih banyak slot!")
        
        return embed
    
    @app_commands.command(name="team", description="View your current battle team")
    async def team_view(self, interaction: discord.Interaction):
        embed = await self.do_team_view(interaction.user.id, interaction.user.display_name)
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name="team")
    async def team_prefix(self, ctx):
        embed = await self.do_team_view(ctx.author.id, ctx.author.display_name)
        await ctx.send(embed=embed)

class AnimalListView(discord.ui.View):
    def __init__(self, cog: AnimalCog, user_id: int, username: str, current_page: int, total_pages: int):
        super().__init__(timeout=60)
        self.cog = cog
        self.user_id = user_id
        self.username = username
        self.current_page = current_page
        self.total_pages = total_pages
        
        self.update_buttons()
    
    def update_buttons(self):
        self.prev_button.disabled = self.current_page <= 1
        self.next_button.disabled = self.current_page >= self.total_pages
    
    @discord.ui.button(label="◀️ Prev", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ini bukan daftar hewanmu!", ephemeral=True)
            return
        
        self.current_page -= 1
        embed, _, _ = await self.cog.do_animal_list(self.user_id, self.username, self.current_page)
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ini bukan daftar hewanmu!", ephemeral=True)
            return
        
        self.current_page += 1
        embed, _, _ = await self.cog.do_animal_list(self.user_id, self.username, self.current_page)
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

async def setup(bot):
    await bot.add_cog(AnimalCog(bot))
