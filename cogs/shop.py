import logging
import json
import asyncio

from utils.database import db_functions as db
from utils.functions_ import is_empty

from discord import Embed, Colour
from discord.ext.commands import Bot, Cog, command

log = logging.getLogger('bot.' + __name__)


with open('jsons/shop.json', 'r') as f:
    data = json.load(f)


class ShopCog(Cog, name='Shop'):
    """Commands related to the shop."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = self.bot.config

    @command(name="shop")
    async def shop_cmd(self, ctx):
        desc = "Current materials and their values. \n"
        for item in data[0]:
            desc += f"**{item}:** {data[0][item]} gold. \n"
        embed = Embed(title="Shop", colour=Colour.blurple(), description=desc)
        embed.set_footer(text="Use `!sell {item}` to sell an item.")
        return await ctx.send(embed=embed)

    @command(name="sell")
    async def sell_item(self, ctx, item_to_sell):
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        channel = ctx.channel
        user_id = ctx.author.id
        for item in list(data[0]):
            if item.lower() == item_to_sell.lower():
                item_to_sell = item
                item_exists = True
        if 'item_exists' in locals():
            sql = "SELECT " + item_to_sell.lower() + " FROM inventory WHERE character_id = %s"
            val = user_id
            await cursor.execute(sql, (val,))
            result = await cursor.fetchall()
            amount = result[0][0]
            if amount > 0:
                await ctx.send(f"You have {amount} {item_to_sell}. How much would you like to sell?")
                try:
                    def check(m):
                        return m.channel == channel and ctx.author == m.author
                    msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    return await ctx.send('No response. Action cancelled.')
                amount_to_sell = msg.content
                if amount_to_sell.isdigit() is True:
                    if int(amount_to_sell) > int(amount):
                        return await ctx.send(f"You don't have enough {item_to_sell} to do that.")
                    else:
                        selling_value = data[0][item_to_sell]
                        sold_for = int(selling_value) * int(amount_to_sell)
                        sql = f"UPDATE inventory SET {item_to_sell} = {item_to_sell} - {amount_to_sell}, gold = gold + {sold_for} WHERE character_id = %s"
                        val = user_id
                        await cursor.execute(sql, (val,))
                        await db_connection.commit()
                        await cursor.close()
                        db_connection.close()
                        return await ctx.send(f"Sold {amount_to_sell} {item_to_sell} for {sold_for} gold.")
                else:
                    return await ctx.send("You have to submit a valid amount.")
            else:
                return await ctx.send("Sorry you do not have enough of that item in order to sell it.")
        else:
            return await ctx.send("The item you are trying to sell does not exist.")

    @command(name="autosell")
    async def autosell_cmd(self, ctx):
        user_id = ctx.author.id
        sql = "SELECT autosell FROM `character` WHERE user_id = '%s'"
        val = user_id
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        await cursor.execute(sql, (val,))
        result = await cursor.fetchall()
        autosell = result[0][0]
        if autosell == 'true':
            sql = "UPDATE `character` SET autosell = %s"
            val = 'false'
            await cursor.execute(sql, (val,))
            await db_connection.commit()
            await cursor.close()
            db_connection.close()
            return await ctx.send("Turned autosell off. This command can be used any time to turn it on.")
        if autosell == 'false':
            sql = "UPDATE `character` SET autosell = %s"
            val = 'true'
            await cursor.execute(sql, (val,))
            await db_connection.commit()
            await cursor.close()
            db_connection.close()
            return await ctx.send("Turned autosell on. This command can be used any time to turn it off.")


def setup(bot):
    bot.add_cog(ShopCog(bot))
    log.debug('Loaded')
