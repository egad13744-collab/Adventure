import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio

GAMBLE_COOLDOWN = 10

class MinigamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.guess_games = {}
    
    async def check_gamble_cooldown(self, user_id: int):
        cooldown = await self.db.check_cooldown(user_id, 'last_gamble', GAMBLE_COOLDOWN)
        return cooldown
    
    @app_commands.command(name="guess", description="Play a number guessing game!")
    @app_commands.describe(bet="Amount of coins to bet (10-1000)")
    async def guess(self, interaction: discord.Interaction, bet: int = 50):
        await self.do_guess(interaction, interaction.user.id, interaction.user.name, bet, is_slash=True)
    
    @commands.command(name="guess")
    async def guess_prefix(self, ctx, bet: int = 50):
        await self.do_guess(ctx, ctx.author.id, ctx.author.name, bet, is_slash=False)
    
    async def do_guess(self, ctx_or_interaction, user_id: int, username: str, bet: int, is_slash: bool):
        if user_id in self.guess_games:
            msg = "❌ Kamu sudah punya game tebak angka yang sedang berjalan!"
            if is_slash:
                await ctx_or_interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_interaction.send(msg)
            return
        
        cooldown = await self.check_gamble_cooldown(user_id)
        if cooldown:
            msg = f"⏳ Tunggu **{cooldown}** detik sebelum bermain lagi!"
            if is_slash:
                await ctx_or_interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_interaction.send(msg)
            return
        
        if bet < 10 or bet > 1000:
            msg = "❌ Taruhan harus antara 10 dan 1000 koin!"
            if is_slash:
                await ctx_or_interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_interaction.send(msg)
            return
        
        user = await self.db.get_user(user_id, username)
        if user['coins'] < bet:
            msg = f"❌ Koin tidak cukup! Kamu punya **{user['coins']:,}** koin."
            if is_slash:
                await ctx_or_interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_interaction.send(msg)
            return
        
        await self.db.set_cooldown(user_id, 'last_gamble')
        
        secret_number = random.randint(1, 10)
        self.guess_games[user_id] = {
            "number": secret_number,
            "bet": bet,
            "attempts": 3
        }
        
        embed = discord.Embed(
            title="🎲 Game Tebak Angka",
            description=f"Aku memikirkan angka antara **1** dan **10**!\n\n"
                        f"💰 Taruhanmu: **{bet}** koin\n"
                        f"🎯 Kesempatan: **3**\n\n"
                        f"Ketik angka di chat untuk menebak!",
            color=discord.Color.blue()
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
            channel = ctx_or_interaction.channel
        else:
            await ctx_or_interaction.send(embed=embed)
            channel = ctx_or_interaction.channel
        
        def check(m):
            return m.author.id == user_id and m.channel.id == channel.id and m.content.isdigit()
        
        try:
            while user_id in self.guess_games and self.guess_games[user_id]["attempts"] > 0:
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess = int(msg.content)
                
                if guess < 1 or guess > 10:
                    await msg.reply("Silakan tebak angka antara 1 dan 10!")
                    continue
                
                game = self.guess_games[user_id]
                
                if guess == game["number"]:
                    winnings = game["bet"] * 2
                    await self.db.add_coins(user_id, winnings - game["bet"])
                    
                    win_embed = discord.Embed(
                        title="🎉 Benar!",
                        description=f"Angkanya adalah **{game['number']}**!\n\n"
                                    f"💰 Kamu menang **{winnings}** koin!",
                        color=discord.Color.green()
                    )
                    await msg.reply(embed=win_embed)
                    del self.guess_games[user_id]
                    return
                else:
                    game["attempts"] -= 1
                    hint = "Lebih tinggi!" if guess < game["number"] else "Lebih rendah!"
                    
                    if game["attempts"] > 0:
                        await msg.reply(f"❌ Salah! {hint} Sisa **{game['attempts']}** kesempatan.")
                    else:
                        await self.db.add_coins(user_id, -game["bet"])
                        
                        lose_embed = discord.Embed(
                            title="😢 Game Over!",
                            description=f"Angkanya adalah **{game['number']}**!\n\n"
                                        f"💸 Kamu kalah **{game['bet']}** koin!",
                            color=discord.Color.red()
                        )
                        await msg.reply(embed=lose_embed)
                        del self.guess_games[user_id]
                        return
                        
        except asyncio.TimeoutError:
            if user_id in self.guess_games:
                game = self.guess_games[user_id]
                await self.db.add_coins(user_id, -game["bet"])
                
                if is_slash:
                    await ctx_or_interaction.followup.send(
                        f"⏰ Waktu habis! Angkanya adalah **{game['number']}**. Kamu kalah **{game['bet']}** koin!"
                    )
                else:
                    await channel.send(
                        f"⏰ Waktu habis! Angkanya adalah **{game['number']}**. Kamu kalah **{game['bet']}** koin!"
                    )
                del self.guess_games[user_id]
    
    @app_commands.command(name="slots", description="Try your luck at the slot machine!")
    @app_commands.describe(bet="Amount of coins to bet (10-500)")
    async def slots(self, interaction: discord.Interaction, bet: int = 50):
        embed, error = await self.do_slots(interaction.user.id, interaction.user.name, bet)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed)
    
    @commands.command(name="slots")
    async def slots_prefix(self, ctx, bet: int = 50):
        embed, error = await self.do_slots(ctx.author.id, ctx.author.name, bet)
        if error:
            await ctx.send(error)
        else:
            await ctx.send(embed=embed)
    
    async def do_slots(self, user_id: int, username: str, bet: int):
        cooldown = await self.check_gamble_cooldown(user_id)
        if cooldown:
            return None, f"⏳ Tunggu **{cooldown}** detik sebelum bermain lagi!"
        
        if bet < 10 or bet > 500:
            return None, "❌ Taruhan harus antara 10 dan 500 koin!"
        
        user = await self.db.get_user(user_id, username)
        if user['coins'] < bet:
            return None, f"❌ Koin tidak cukup! Kamu punya **{user['coins']:,}** koin."
        
        await self.db.set_cooldown(user_id, 'last_gamble')
        
        symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣', '⭐']
        weights = [30, 25, 20, 15, 6, 3, 1]
        
        result = random.choices(symbols, weights=weights, k=3)
        
        multiplier = 0
        if result[0] == result[1] == result[2]:
            if result[0] == '7️⃣':
                multiplier = 10
            elif result[0] == '💎':
                multiplier = 7
            elif result[0] == '⭐':
                multiplier = 15
            else:
                multiplier = 5
        elif result[0] == result[1] or result[1] == result[2]:
            multiplier = 2
        
        winnings = bet * multiplier
        net = winnings - bet
        
        await self.db.add_coins(user_id, net)
        
        slot_display = f"╔═══════════╗\n║ {' '.join(result)} ║\n╚═══════════╝"
        
        if multiplier > 0:
            color = discord.Color.green()
            if multiplier >= 10:
                title = "🎰 JACKPOT!!!"
            elif multiplier >= 5:
                title = "🎰 MENANG BESAR!"
            else:
                title = "🎰 Menang!"
            result_text = f"💰 Kamu menang **{winnings}** koin! (x{multiplier})"
        else:
            color = discord.Color.red()
            title = "🎰 Tidak Beruntung..."
            result_text = f"💸 Kamu kalah **{bet}** koin!"
        
        embed = discord.Embed(
            title=title,
            description=f"```\n{slot_display}\n```\n{result_text}",
            color=color
        )
        
        new_balance = user['coins'] + net
        embed.set_footer(text=f"Saldo: {new_balance:,} koin")
        
        return embed, None

async def setup(bot):
    await bot.add_cog(MinigamesCog(bot))
