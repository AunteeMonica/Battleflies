from classes import battleflyBotCog
from cogs.logic import TheSproutLogic
from discord.ext import commands
from events import EventManager
from modules.battleflybot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    NightVendorSaleAlreadyMadeException,
    NotEnoughRerollsException,
    UnavailablebattleflyToTradeException
)


class TheSproutCommands(battleflyBotCog):

    def __init__(self, bot):
        super().__init__()
        self.event_manager = EventManager(bot)
        event = self.event_manager.get_event_by_key("the_sprout")
        self.sprout_logic = TheSproutLogic(
            bot,
            event
        )

    def _is_event_active(self) -> bool:
        """
        Checks if the event is active
        """
        return self.event_manager.is_event_active("the_sprout")

    async def _post_sprout_inactive_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Posts the message specifying that The Sprout is unavailable
        """
        await ctx.send(f"{ctx.message.author.mention},"
                       " The Sprout is currently unavailable.")

    @commands.command(name='sprout', pass_context=True)
    async def sprout(self, ctx: commands.Context) -> None:
        """
        Displays what The Sprout wants to trade
        """
        try:
            if self._is_event_active():
                msg = self.sprout_logic.build_sprout_offer_msg(ctx)
                await ctx.send(msg)
            else:
                await self._post_sprout_inactive_msg(ctx)
        except NightVendorSaleAlreadyMadeException:
            await self.sprout_sale_already_made_msg(ctx)

    @commands.command(name='sproutroll', pass_context=True)
    async def sproutroll(self, ctx: commands.Context) -> None:
        """
        Re-rolls what The Sprout has to offer
        """
        try:
            if self._is_event_active():
                self.sprout_logic.reroll_sprout_offer(ctx)
                msg = self.sprout_logic.build_sprout_offer_msg(ctx)
                await ctx.send(msg)
            else:
                await self._post_sprout_inactive_msg(ctx)
        except NightVendorSaleAlreadyMadeException:
            await self.sprout_sale_already_made_msg(ctx)
        except NotEnoughRerollsException:
            await self.not_enough_reroll_msg(ctx)

    @commands.command(name='sprouttrade', pass_context=True)
    async def sprouttrade(self, ctx: commands.Context) -> None:
        """
        Confirms The Sprout trade
        """
        try:
            if self._is_event_active():
                msg = await self.sprout_logic.trade_sprout(ctx)
                await ctx.send(msg)
            else:
                await self._post_sprout_inactive_msg(ctx)
        except HigherReleaseQuantitySpecifiedException:
            await self.higher_quantity_specified_msg(ctx)
        except NightVendorSaleAlreadyMadeException:
            await self.sprout_sale_already_made_msg(ctx)
        except UnavailablebattleflyToTradeException as e:
            await self.unavailable_battlefly_to_trade_msg(ctx, e)
