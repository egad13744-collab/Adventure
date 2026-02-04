import discord
from discord import app_commands
from discord.ext import commands
from data.items import get_item, SKINS, WEAPONS, FISHING_RODS

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    async def create_profile_embed(self, target):
        profile = await self.db.get_user(target.id, target.name)
        battle_stats = await self.db.get_battle_stats(target.id)
        
        exp_needed = self.db.exp_for_level(profile['level'])
        progress = int((profile['exp'] / exp_needed) * 10)
        progress_bar = "█" * progress + "░" * (10 - progress)
        
        embed = discord.Embed(
            title=f"⚔️ Profil {target.display_name}",
            color=discord.Color.blue()
        )
        
        embed.set_thumbnail(url=target.display_avatar.url)
        
        embed.add_field(
            name="📊 Stats",
            value=f"**Level:** {profile['level']}\n"
                  f"**EXP:** {profile['exp']}/{exp_needed}\n"
                  f"[{progress_bar}]",
            inline=True
        )
        
        embed.add_field(
            name="💰 Ekonomi",
            value=f"**Koin:** {profile['coins']:,}\n"
                  f"**Daily Streak:** {profile['daily_streak']} 🔥",
            inline=True
        )
        
        equipped_weapon = "Tidak ada"
        equipped_rod = "Tidak ada"
        equipped_skin = "Tidak ada"
        
        if profile['equipped_weapon']:
            item = get_item(profile['equipped_weapon'])
            if item:
                equipped_weapon = f"{item['emoji']} {item['name']}"
        
        if profile['equipped_rod']:
            item = get_item(profile['equipped_rod'])
            if item:
                equipped_rod = f"{item['emoji']} {item['name']}"
        
        if profile['equipped_skin']:
            item = get_item(profile['equipped_skin'])
            if item:
                equipped_skin = f"{item['emoji']} {item['name']}"
        
        embed.add_field(
            name="🎒 Equipment",
            value=f"**Senjata:** {equipped_weapon}\n"
                  f"**Joran:** {equipped_rod}\n"
                  f"**Skin:** {equipped_skin}",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ Battle Stats",
            value=f"**Menang:** {battle_stats['wins']}\n"
                  f"**Kalah:** {battle_stats['losses']}\n"
                  f"**Monster Dibunuh:** {battle_stats['monsters_killed']}",
            inline=True
        )
        
        embed.set_footer(text="Gunakan /help atau qhelp untuk melihat semua command!")
        
        return embed
    
    @app_commands.command(name="profile", description="View your adventure profile")
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        target = user or interaction.user
        embed = await self.create_profile_embed(target)
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name="profile")
    async def profile_prefix(self, ctx, user: discord.User = None):
        target = user or ctx.author
        embed = await self.create_profile_embed(target)
        await ctx.send(embed=embed)
    
    async def do_equip(self, user_id: int, item_id: str):
        has_item = await self.db.has_item(user_id, item_id)
        if not has_item:
            return None, "❌ Kamu tidak punya item ini di inventory!"
        
        item = get_item(item_id)
        if not item:
            return None, "❌ ID item tidak valid!"
        
        if item_id in WEAPONS:
            await self.db.update_user(user_id, equipped_weapon=item_id)
            slot = "senjata"
        elif item_id in FISHING_RODS:
            await self.db.update_user(user_id, equipped_rod=item_id)
            slot = "joran"
        elif item_id in SKINS:
            await self.db.update_user(user_id, equipped_skin=item_id)
            slot = "skin"
        else:
            return None, "❌ Item ini tidak bisa dipakai!"
        
        embed = discord.Embed(
            title="✅ Item Dipakai!",
            description=f"Kamu memakai **{item['emoji']} {item['name']}** sebagai {slot}!",
            color=item['rarity'].color
        )
        
        return embed, None
    
    @app_commands.command(name="equip", description="Equip an item from your inventory")
    @app_commands.describe(item_id="The ID of the item to equip")
    async def equip(self, interaction: discord.Interaction, item_id: str):
        embed, error = await self.do_equip(interaction.user.id, item_id)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed)
    
    @commands.command(name="equip")
    async def equip_prefix(self, ctx, item_id: str = None):
        if not item_id:
            await ctx.send("❌ Penggunaan: `qequip <item_id>`")
            return
        embed, error = await self.do_equip(ctx.author.id, item_id)
        if error:
            await ctx.send(error)
        else:
            await ctx.send(embed=embed)
    
    @app_commands.command(name="unequip", description="Unequip an item")
    @app_commands.describe(slot="The slot to unequip (weapon, rod, skin)")
    @app_commands.choices(slot=[
        app_commands.Choice(name="Weapon", value="weapon"),
        app_commands.Choice(name="Fishing Rod", value="rod"),
        app_commands.Choice(name="Skin", value="skin"),
    ])
    async def unequip(self, interaction: discord.Interaction, slot: str):
        user_id = interaction.user.id
        
        if slot == "weapon":
            await self.db.update_user(user_id, equipped_weapon=None)
        elif slot == "rod":
            await self.db.update_user(user_id, equipped_rod=None)
        elif slot == "skin":
            await self.db.update_user(user_id, equipped_skin=None)
        
        await interaction.response.send_message(
            f"✅ {slot} dilepas!",
            ephemeral=True
        )
    
    @commands.command(name="unequip")
    async def unequip_prefix(self, ctx, slot: str = None):
        if not slot or slot not in ["weapon", "rod", "skin"]:
            await ctx.send("❌ Penggunaan: `qunequip <weapon/rod/skin>`")
            return
        
        if slot == "weapon":
            await self.db.update_user(ctx.author.id, equipped_weapon=None)
        elif slot == "rod":
            await self.db.update_user(ctx.author.id, equipped_rod=None)
        elif slot == "skin":
            await self.db.update_user(ctx.author.id, equipped_skin=None)
        
        await ctx.send(f"✅ {slot} dilepas!")

async def setup(bot):
    await bot.add_cog(ProfileCog(bot))
