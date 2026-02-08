import discord
from discord import app_commands
from discord.ext import commands

class PrestigeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    async def do_prestige(self, user_id: int, username: str):
        user = await self.db.get_user(user_id, username)
        current_level = user['level']
        prestige_level = user.get('prestige_level', 0)
        
        # Requirement: Level 100 + (prestige * 50)
        req_level = 100 + (prestige_level * 50)
        
        if current_level < req_level:
            return f"❌ Kamu butuh Level **{req_level}** untuk Prestige! (Level saat ini: {current_level})"

        # Prestige logic: Reset level, exp, coins
        new_prestige = prestige_level + 1
        
        # Perform reset in DB
        pool = await self.db.get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                # Update user stats
                await conn.execute(
                    'UPDATE users SET level = 1, exp = 0, coins = 100, prestige_level = $1 WHERE user_id = $2',
                    new_prestige, user_id
                )
                # Reset all animals level but keep them? 
                # Request was to "perbaiki prestige", usually it's a full reset for bonuses.
                # For safety, we only reset player stats and give bonuses via prestige_level.
        
        return f"✨ **CONGRATULATIONS!** ✨\nKamu telah mencapai Prestige Level **{new_prestige}**!\nLevelmu telah direset ke 1, tapi kamu mendapatkan bonus EXP permanen!"

    @app_commands.command(name="prestige", description="Reset your level for permanent bonuses!")
    async def prestige_slash(self, interaction: discord.Interaction):
        message = await self.do_prestige(interaction.user.id, interaction.user.name)
        await interaction.response.send_message(message)

    @commands.command(name="prestige")
    async def prestige_prefix(self, ctx):
        message = await self.do_prestige(ctx.author.id, ctx.author.name)
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(PrestigeCog(bot))
