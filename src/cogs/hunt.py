import discord
from discord import app_commands
from discord.ext import commands
import random
from data.animals import get_random_animal, ANIMALS, get_animal_by_id
from data.items import Rarity, get_item
from utils.emoji_utils import get_animal_emoji

HUNT_COOLDOWN = 10

class HuntCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    def get_bonuses(self, profile):  
        exp_bonus = 0  
        coin_bonus = 0  
        luck_bonus = 0  

        if profile.get('equipped_skin'):  
            skin = get_item(profile['equipped_skin'])  
            if skin:  
                exp_bonus += skin.get('exp_bonus', 0)  
                coin_bonus += skin.get('coin_bonus', 0)  
                luck_bonus += skin.get('luck_bonus', 0)  

        return exp_bonus, coin_bonus, luck_bonus  

    async def do_hunt(self, user_id: int, username: str):  
        profile = await self.db.get_user(user_id, username)  

        cooldown = await self.db.check_cooldown(user_id, 'last_hunt', HUNT_COOLDOWN)  
        if cooldown:  
            return None, f"⏳ Kamu masih lelah dari perburuan terakhir! Tunggu **{cooldown}** detik."  

        exp_bonus, coin_bonus, luck_bonus = self.get_bonuses(profile)  

        animal = get_random_animal(luck_bonus)  
        animal_uuid = await self.db.add_animal(user_id, animal)  

        base_exp = random.randint(5, 15)  
        base_coins = random.randint(3, 10)  

        exp_gained = int(base_exp * (1 + exp_bonus / 100))  
        coins_gained = int(base_coins * (1 + coin_bonus / 100))  

        await self.db.add_coins(user_id, coins_gained)  
        level_result = await self.db.add_exp(user_id, exp_gained)  
        await self.db.set_cooldown(user_id, 'last_hunt')  

        hunt_messages = [  
            "Kamu menjelajahi hutan gelap...",  
            "Kamu mencari di reruntuhan kuno...",  
            "Kamu mendaki gunung berbahaya...",  
            "Kamu menyusuri gua misterius...",  
            "Kamu melewati rawa mistis...",  
        ]  

        embed = discord.Embed(  
            title="🏹 Hasil Berburu",  
            description=random.choice(hunt_messages),  
            color=animal['rarity'].color  
        )  

        animal_emoji = get_animal_emoji(animal['animal_id'])  
        skill_info = f"**Skill:** {animal['skill']['name']}\n*{animal['skill']['effect']}*"  

        embed.add_field(  
            name=f"🎉 Hewan Tertangkap!",  
            value=f"{animal_emoji} **{animal['name']}** ({animal['rarity'].display_name})\n\n"  
                  f"❤️ HP: {animal['hp']} | ⚔️ ATK: {animal['attack']} | 🛡️ DEF: {animal['defense']}\n"  
                  f"{skill_info}\n\n"  
                  f"🆔 ID: `{animal_uuid}`",  
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
            Rarity.RARE: "Tangkapan bagus! Itu hewan langka!",  
            Rarity.EPIC: "Luar biasa! Hewan epik!",  
            Rarity.LEGENDARY: "LEGENDARIS! Kamu sangat beruntung!",  
            Rarity.MYTHIC: "MYTHIC! Ini sangat langka!",  
            Rarity.EXOTIC: "EXOTIC! Hewan super langka!",  
            Rarity.CELESTIAL: "CELESTIAL! Makhluk surgawi!",  
            Rarity.SECRET: "SECRET! Hewan tersembunyi legendaris!"  
        }  

        if animal['rarity'] in rarity_tips:  
            embed.set_footer(text=rarity_tips[animal['rarity']])  
        else:  
            embed.set_footer(text=f"Cooldown: {HUNT_COOLDOWN}s | Gunakan /animal list untuk melihat hewanmu")  

        return embed, None  

    @app_commands.command(name="hunt", description="Hunt to capture wild animals for your team!")  
    async def hunt(self, interaction: discord.Interaction):  
        embed, error = await self.do_hunt(interaction.user.id, interaction.user.name)  
        if error:  
            await interaction.response.send_message(error, ephemeral=True)  
        elif embed:  
            await interaction.response.send_message(embed=embed)  

    @commands.command(name="hunt")  
    async def hunt_prefix(self, ctx):  
        embed, error = await self.do_hunt(ctx.author.id, ctx.author.name)  
        if error:  
            await ctx.send(error)  
        else:  
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HuntCog(bot))
