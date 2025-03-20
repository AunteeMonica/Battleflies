from discord.ext import commands

class BattleflyBotCog(commands.Cog):
    def __init__(self):
        super().__init__()
        print(f"Added {type(self).__name__} Cog")

    async def battlefly_does_not_exist_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, the battlefly '**{str(e)}**' does not exist. Please specify a valid battlefly name.")

    async def catch_cooldown_incomplete_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please wait **{str(e)}** second(s) to catch another battlefly.")

    async def daily_cooldown_incomplete_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you've already claimed the daily for today.")

    async def higher_quantity_specified_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify a battlefly quantity less than or equal to the max allowed: **{str(e)}**")

    async def higher_page_specified_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify a page number less than the max page number: **{str(e)}**")

    async def invalid_daily_shop_item_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify an item from the daily shop menu from **1** to **{str(e)}**.")

    async def cocoon_does_not_exist_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify a valid cocoon to open (**{str(e)}** does not exist).")

    async def no_egg_count_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you have no {str(e)} eggs to hatch.")

    async def not_enough_daily_tokens_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you need **{str(e)}** daily tokens to buy this item.")

    async def not_enough_exchange_battlefly_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify a valid number of battleflies to exchange.")

    async def not_enough_cocoon_quantity_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please make sure you have enough **{str(e)}** cocoons to open.")

    async def not_enough_reroll_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you've used up all your re-rolls.")

    async def sprout_sale_already_made_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you've already traded with The Sprout.")

    async def page_quantity_too_low_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify an inventory page number greater than 0.")

    async def release_quantity_too_low_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify a battlefly quantity greater than 0 to release.")

    async def too_many_exchange_battlefly_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify only 5 battleflies to exchange.")

    async def unavailable_battlefly_to_trade_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you're missing a **{str(e).title()}** to trade with The Sprout.")

    async def unregistered_ally_msg(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.message.author.mention}, you haven't started your journey as an Ally yet. Catch a battlefly first to begin!")

    async def unregistered_ally_admin_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, <@{str(e)}> hasn't started their journey as an Ally yet.")
