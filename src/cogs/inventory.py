import discord
from discord import app_commands
from discord.ext import commands
from data.items import get_item, ALL_ITEMS, Rarity

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    async def create_inventory_embed(self, user_id: int, username: str, display_name: str):
        await self.db.get_user(user_id, username)
        inventory = await self.db.get_inventory(user_id)
        
        if not inventory:
            embed = discord.Embed(
                title="🎒 Inventorymu",
                description="Inventorymu kosong!\nGunakan `/hunt` atau `/fish` untuk mendapat item.",
                color=discord.Color.orange()
            )
            return embed
        
        categorized = {
            "hunt_loot": [],
            "fish_loot": [],
            "weapons": [],
            "rods": [],
            "skins": [],
            "other": []
        }
        
        from data.items import HUNT_LOOT, FISH_LOOT, WEAPONS, FISHING_RODS, SKINS
        
        for inv_item in inventory:
            item_id = inv_item['item_id']
            quantity = inv_item['quantity']
            item = get_item(item_id)
            
            if not item:
                continue
            
            item_str = f"{item['emoji']} {item['name']} x{quantity}"
            
            if item_id in HUNT_LOOT:
                categorized["hunt_loot"].append(item_str)
            elif item_id in FISH_LOOT:
                categorized["fish_loot"].append(item_str)
            elif item_id in WEAPONS:
                categorized["weapons"].append(item_str)
            elif item_id in FISHING_RODS:
                categorized["rods"].append(item_str)
            elif item_id in SKINS:
                categorized["skins"].append(item_str)
            else:
                categorized["other"].append(item_str)
        
        embed = discord.Embed(
            title=f"🎒 Inventory {display_name}",
            color=discord.Color.green()
        )
        
        if categorized["weapons"]:
            embed.add_field(
                name="⚔️ Senjata",
                value="\n".join(categorized["weapons"]),
                inline=False
            )
        
        if categorized["rods"]:
            embed.add_field(
                name="🎣 Joran",
                value="\n".join(categorized["rods"]),
                inline=False
            )
        
        if categorized["skins"]:
            embed.add_field(
                name="👔 Skin",
                value="\n".join(categorized["skins"]),
                inline=False
            )
        
        if categorized["hunt_loot"]:
            embed.add_field(
                name="🏹 Hasil Berburu",
                value="\n".join(categorized["hunt_loot"][:10]) + 
                      (f"\n... dan {len(categorized['hunt_loot']) - 10} lainnya" if len(categorized['hunt_loot']) > 10 else ""),
                inline=False
            )
        
        if categorized["fish_loot"]:
            embed.add_field(
                name="🐟 Ikan",
                value="\n".join(categorized["fish_loot"][:10]) +
                      (f"\n... dan {len(categorized['fish_loot']) - 10} lainnya" if len(categorized['fish_loot']) > 10 else ""),
                inline=False
            )
        
        embed.set_footer(text="Gunakan /sell atau qsell untuk menjual | /equip atau qequip untuk memakai")
        
        return embed
    
    @app_commands.command(name="inventory", description="View your inventory")
    async def inventory(self, interaction: discord.Interaction):
        embed = await self.create_inventory_embed(
            interaction.user.id, 
            interaction.user.name, 
            interaction.user.display_name
        )
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name="inventory", aliases=["inv"])
    async def inventory_prefix(self, ctx):
        embed = await self.create_inventory_embed(
            ctx.author.id, 
            ctx.author.name, 
            ctx.author.display_name
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
