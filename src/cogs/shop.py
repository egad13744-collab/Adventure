import discord
from discord import app_commands
from discord.ext import commands
from data.items import WEAPONS, FISHING_RODS, SKINS, get_item, ALL_ITEMS, Rarity, get_rarity_by_code, RARITY_SELL_PRICES
from data.animals import get_animal_by_id

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    @app_commands.command(name="shop", description="Browse the adventure shop")
    @app_commands.describe(category="Shop category to browse")
    @app_commands.choices(category=[
        app_commands.Choice(name="Weapons", value="weapons"),
        app_commands.Choice(name="Fishing Rods", value="rods"),
        app_commands.Choice(name="Skins", value="skins"),
    ])
    async def shop(self, interaction: discord.Interaction, category: str = "weapons"):
        embed = await self.create_shop_embed(interaction.user.id, interaction.user.name, category)
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name="shop")
    async def shop_prefix(self, ctx, category: str = "weapons"):
        embed = await self.create_shop_embed(ctx.author.id, ctx.author.name, category)
        await ctx.send(embed=embed)
    
    async def create_shop_embed(self, user_id: int, username: str, category: str):
        user = await self.db.get_user(user_id, username)
        
        if category == "weapons":
            items = WEAPONS
            title = "⚔️ Toko Senjata"
            description = "Senjata lebih kuat = lebih banyak damage!"
        elif category == "rods":
            items = FISHING_RODS
            title = "🎣 Toko Joran"
            description = "Joran lebih baik = keberuntungan lebih tinggi!"
        else:
            items = SKINS
            title = "👔 Toko Skin"
            description = "Skin memberikan bonus EXP, koin, dan keberuntungan!"
        
        embed = discord.Embed(
            title=title,
            description=f"{description}\n\n💰 Koinmu: **{user['coins']:,}**",
            color=discord.Color.gold()
        )
        
        for item_id, item in items.items():
            if 'buy_price' not in item:
                continue
                
            stats = []
            if 'attack' in item:
                stats.append(f"Attack: +{item['attack']}")
            if 'luck_bonus' in item:
                stats.append(f"Luck: +{item['luck_bonus']}%")
            if 'exp_bonus' in item:
                stats.append(f"EXP: +{item['exp_bonus']}%")
            if 'coin_bonus' in item:
                stats.append(f"Koin: +{item['coin_bonus']}%")
            
            stats_str = " | ".join(stats) if stats else "Tidak ada stats khusus"
            
            embed.add_field(
                name=f"{item['emoji']} {item['name']} ({item['rarity'].display_name})",
                value=f"💰 **{item['buy_price']:,}** koin\n{stats_str}\n`/buy {item_id}` atau `qbuy {item_id}`",
                inline=True
            )
        
        embed.set_footer(text="Gunakan /buy <item_id> atau qbuy <item_id> untuk membeli")
        
        return embed
    
    @app_commands.command(name="buy", description="Buy an item from the shop")
    @app_commands.describe(item_id="The ID of the item to buy")
    async def buy(self, interaction: discord.Interaction, item_id: str):
        result = await self.do_buy(interaction.user.id, interaction.user.name, item_id)
        if isinstance(result, discord.Embed):
            await interaction.response.send_message(embed=result)
        else:
            await interaction.response.send_message(result, ephemeral=True)
    
    @commands.command(name="buy")
    async def buy_prefix(self, ctx, item_id: str = None):
        if not item_id:
            await ctx.send("❌ Penggunaan: `qbuy <item_id>`")
            return
        result = await self.do_buy(ctx.author.id, ctx.author.name, item_id)
        if isinstance(result, discord.Embed):
            await ctx.send(embed=result)
        else:
            await ctx.send(result)
    
    async def do_buy(self, user_id: int, username: str, item_id: str):
        user = await self.db.get_user(user_id, username)
        
        item = get_item(item_id)
        if not item or 'buy_price' not in item:
            return "❌ Item ini tidak tersedia untuk dibeli!"
        
        if user['coins'] < item['buy_price']:
            return f"❌ Kamu butuh **{item['buy_price']:,}** koin tapi hanya punya **{user['coins']:,}**!"
        
        await self.db.add_coins(user_id, -item['buy_price'])
        await self.db.add_item(user_id, item_id)
        
        embed = discord.Embed(
            title="✅ Pembelian Berhasil!",
            description=f"Kamu membeli **{item['emoji']} {item['name']}** seharga **{item['buy_price']:,}** koin!",
            color=discord.Color.green()
        )
        embed.set_footer(text="Gunakan /equip atau qequip untuk memakai item barumu!")
        
        return embed
    
    @app_commands.command(name="sell", description="Sell an item or animals by rarity")
    @app_commands.describe(
        item_type="What to sell (item or animal)",
        item_id="Item ID or Rarity code (C/U/R/E/L/M/X/CE/S)"
    )
    async def sell(self, interaction: discord.Interaction, item_type: str, item_id: str, quantity: int = 1):
        if item_type.lower() == "animal":
            result = await self.do_sell_animals_by_rarity(interaction.user.id, item_id)
        else:
            result = await self.do_sell_item(interaction.user.id, item_id, quantity)
        
        if isinstance(result, discord.Embed):
            await interaction.response.send_message(embed=result)
        else:
            await interaction.response.send_message(result, ephemeral=True)
    
    @commands.command(name="sell")
    async def sell_prefix(self, ctx, item_type: str = None, item_id: str = None, quantity: int = 1):
        if not item_type or not item_id:
            await ctx.send("❌ Penggunaan:\n`qsell item <item_id> [quantity]`\n`qsell animal <rarity_code>` (C/U/R/E/L/M/X/CE/S)")
            return
        
        if item_type.lower() == "animal":
            result = await self.do_sell_animals_by_rarity(ctx.author.id, item_id)
        else:
            result = await self.do_sell_item(ctx.author.id, item_id, quantity)
        
        if isinstance(result, discord.Embed):
            await ctx.send(embed=result)
        else:
            await ctx.send(result)
    
    async def do_sell_item(self, user_id: int, item_id: str, quantity: int):
        if quantity < 1:
            return "❌ Jumlah harus minimal 1!"
        
        item = get_item(item_id)
        if not item:
            return "❌ ID item tidak valid!"
        
        if 'sell_price' not in item:
            sell_price = item.get('buy_price', 10) // 2
        else:
            sell_price = item['sell_price']
        
        success = await self.db.remove_item(user_id, item_id, quantity)
        if not success:
            return f"❌ Kamu tidak punya {quantity}x {item['name']} di inventorymu!"
        
        total_coins = sell_price * quantity
        await self.db.add_coins(user_id, total_coins)
        
        embed = discord.Embed(
            title="💰 Item Terjual!",
            description=f"Kamu menjual **{quantity}x {item['emoji']} {item['name']}** seharga **{total_coins:,}** koin!",
            color=discord.Color.gold()
        )
        
        return embed
    
    async def do_sell_animals_by_rarity(self, user_id: int, rarity_code: str):
        rarity = get_rarity_by_code(rarity_code.upper())
        
        if not rarity:
            return f"❌ Kode rarity tidak valid!\nKode yang tersedia: C (Common), U (Uncommon), R (Rare), E (Epic), L (Legendary), M (Mythic), X (Exotic), CE (Celestial), S (Secret)"
        
        animals = await self.db.get_user_animals(user_id)
        
        animals_to_sell = []
        for a in animals:
            if a['is_in_team']:
                continue
            
            animal_data = get_animal_by_id(a['animal_id'])
            if animal_data and animal_data['rarity'] == rarity:
                animals_to_sell.append(a)
        
        if not animals_to_sell:
            return f"❌ Kamu tidak punya hewan **{rarity.display_name}** yang bisa dijual!\n*Note: Hewan di tim tidak bisa dijual.*"
        
        sell_price = RARITY_SELL_PRICES.get(rarity, 10)
        total_coins = len(animals_to_sell) * sell_price
        
        for a in animals_to_sell:
            await self.db.delete_animal(a['id'])
        
        await self.db.add_coins(user_id, total_coins)
        
        embed = discord.Embed(
            title="💰 Hewan Terjual!",
            description=f"Kamu menjual **{len(animals_to_sell)}x** hewan **{rarity.display_name}**\n"
                       f"Harga per hewan: **{sell_price:,}** koin\n\n"
                       f"💵 Total: **{total_coins:,}** koin!",
            color=discord.Color.gold()
        )
        
        return embed

async def setup(bot):
    await bot.add_cog(ShopCog(bot))
