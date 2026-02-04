import discord
from discord import app_commands
from discord.ext import commands
import random
from data.items import FISH_LOOT, Rarity, get_item

FISH_COOLDOWN = 10

class FishCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    def get_bonuses(self, profile):
        exp_bonus = 0
        coin_bonus = 0
        luck_bonus = 0
        
        if profile['equipped_rod']:
            rod = get_item(profile['equipped_rod'])
            if rod:
                luck_bonus += rod.get('luck_bonus', 0)
        
        if profile['equipped_skin']:
            skin = get_item(profile['equipped_skin'])
            if skin:
                exp_bonus += skin.get('exp_bonus', 0)
                coin_bonus += skin.get('coin_bonus', 0)
                luck_bonus += skin.get('luck_bonus', 0)
        
        return exp_bonus, coin_bonus, luck_bonus
    
    def roll_catch(self, luck_bonus: int = 0):
        roll = random.random() * 100
        adjusted_roll = max(0, roll - luck_bonus)
        
        cumulative = 0
        for item_id, item in FISH_LOOT.items():
            cumulative += item['rarity'].drop_chance
            if adjusted_roll <= cumulative:
                return item_id, item
        
        first_item_id = list(FISH_LOOT.keys())[0]
        return first_item_id, FISH_LOOT[first_item_id]
    
    async def do_fish(self, user_id: int, username: str):
        profile = await self.db.get_user(user_id, username)
        
        cooldown = await self.db.check_cooldown(user_id, 'last_fish', FISH_COOLDOWN)
        if cooldown:
            return None, f"⏳ Ikan butuh waktu untuk kembali! Tunggu **{cooldown}** detik."
        
        exp_bonus, coin_bonus, luck_bonus = self.get_bonuses(profile)
        
        item_id, item = self.roll_catch(luck_bonus)
        
        base_exp = random.randint(4, 12)
        base_coins = random.randint(2, 8)
        
        exp_gained = int(base_exp * (1 + exp_bonus / 100))
        coins_gained = int(base_coins * (1 + coin_bonus / 100))
        
        await self.db.add_item(user_id, item_id)
        await self.db.add_coins(user_id, coins_gained)
        level_result = await self.db.add_exp(user_id, exp_gained)
        await self.db.set_cooldown(user_id, 'last_fish')
        
        fish_messages = [
            "Kamu melempar kail ke danau tenang...",
            "Kamu memancing di sungai deras...",
            "Kamu menjelajah kedalaman laut misterius...",
            "Kamu menemukan spot memancing rahasia...",
            "Kamu menunggu dengan sabar di kolam kristal...",
        ]
        
        embed = discord.Embed(
            title="🎣 Hasil Memancing",
            description=random.choice(fish_messages),
            color=item['rarity'].color
        )
        
        embed.add_field(
            name="🐟 Tangkapan",
            value=f"{item['emoji']} **{item['name']}** ({item['rarity'].display_name})",
            inline=False
        )
        
        embed.add_field(
            name="💰 Hadiah",
            value=f"**+{coins_gained}** koin\n**+{exp_gained}** EXP",
            inline=True
        )
        
        if level_result['leveled_up']:
            embed.add_field(
                name="🎉 LEVEL UP!",
                value=f"Kamu mencapai **Level {level_result['new_level']}**!",
                inline=True
            )
        
        rarity_tips = {
            Rarity.RARE: "Tangkapan bagus! Itu langka!",
            Rarity.EPIC: "Tangkapan epik! Keberuntungan luar biasa!",
            Rarity.LEGENDARY: "TANGKAPAN LEGENDARIS! Luar biasa!",
            Rarity.MYTHIC: "TANGKAPAN MYTHIC! Sekali seumur hidup!"
        }
        
        if item['rarity'] in rarity_tips:
            embed.set_footer(text=rarity_tips[item['rarity']])
        else:
            embed.set_footer(text=f"Cooldown: {FISH_COOLDOWN}s | Joran lebih baik = keberuntungan lebih tinggi!")
        
        return embed, None
    
    @app_commands.command(name="fish", description="Go fishing for treasures!")
    async def fish(self, interaction: discord.Interaction):
        embed, error = await self.do_fish(interaction.user.id, interaction.user.name)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed)
    
    @commands.command(name="fish")
    async def fish_prefix(self, ctx):
        embed, error = await self.do_fish(ctx.author.id, ctx.author.name)
        if error:
            await ctx.send(error)
        else:
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FishCog(bot))
