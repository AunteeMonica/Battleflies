from cogs.battleflybot_cog import BattleflyBotCog
from cogs.logic import DailyLogic
from discord.ext import commands
from modules.battleflybot_exceptions import (
    DailyCooldownIncompleteException,
    ImproperDailyShopItemNumberException,
    NotEnoughDailyShopTokensException
)


class DailyCommands(BattleflyBotCog):

    def __init__(self, bot):
        super().__init__()
        self.daily_logic = DailyLogic(bot)

    @commands.command(name='daily', pass_context=True)
    async def daily(self, ctx: commands.Context) -> None:
        """
        Claim a daily cocoon as well as a daily token
        """
        try:
            cocoon = self.daily_logic.claim_daily(ctx)
            await ctx.send(f"{ctx.message.author.mention},"
                           f" you've claimed a **{cocoon}** cocoon"
                           " and a daily token to use in the"
                           " daily token shop")
        except DailyCooldownIncompleteException:
            await self.daily_cooldown_incomplete_msg(ctx)

    @commands.command(name='tokens', pass_context=True)
    async def tokens(self, ctx: commands.Context) -> None:
        """
        Displays the number of daily tokens the user has
        """
        msg = self.daily_logic.build_daily_tokens_msg(ctx)
        await ctx.send(msg)

    @commands.command(name='shop', pass_context=True)
    async def shop(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Displays the daily shop menu
        """
        em = self.daily_logic.get_daily_shop_info()
        await ctx.send(embed=em)

    @commands.command(name='buy', pass_context=True)
    async def buy(
        self,
        ctx: commands.Context,
        item_num: int = commands.parameter(
            description="Number to select which shop item to buy"
        )
    ) -> None:
        try:
            msg = await self.daily_logic.buy_daily_shop_item(ctx, item_num)
            await ctx.send(msg)
        except ImproperDailyShopItemNumberException as e:
            await self.improper_daily_shop_item_number_msg(
                ctx,
                e
            )
        except NotEnoughDailyShopTokensException as e:
            await self.not_enough_daily_shop_tokens_msg(
                ctx,
                e
            )
