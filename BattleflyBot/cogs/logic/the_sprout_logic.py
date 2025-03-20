from modules.battleflybot_module import BattleflyBotModule
from cogs.logic.actions.release_battlefly import ReleasebattleflyAction
from events.the_sprout_event import TheSproutEvent
from modules.battleflybot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    TheSproutLogicException,
    TheSproutSaleAlreadyMadeException,
    NotEnoughRerollsException,
    UnavailableBattleflyToTradeException
)
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_generator import battleflyBotGenerator
from modules.battleflybot_rates import battleflyBotRates
from modules.battleflybot_status import battleflyBotStatus
from modules.services.ally_service import AllyService
from utils import get_ctx_user_id
import discord


class TheSproutLogic(BattleflyBotModule):
    """Handles The Sprout trade logic for BattleflyBot"""

    def __init__(self, bot, event: TheSproutEvent):
        self.assets = battleflyBotAssets()
        self.event = event
        self.rates = battleflyBotRates(bot)
        self.status = battleflyBotStatus(bot)
        self.generator = battleflyBotGenerator(self.assets, self.rates)
        self.ally_service = AllyService(self.rates)
        self.release_battlefly_action = ReleasebattleflyAction(
            self.assets,
            self.status,
            self.ally_service,
        )

    def build_sprout_offer_msg(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Builds the message for The Sprout’s trade offer
        """
        try:
            user_id = get_ctx_user_id(ctx)
            if self.event.check_user_traded(user_id):
                raise TheSproutSaleAlreadyMadeException()
            if not self.event.check_user_has_offer(user_id):
                self.event.create_or_update_roll_count(user_id)
                self._create_sprout_offer(user_id)
            sprout_battlefly = self.event.get_sprout_offered_battlefly(user_id)
            if self.event.get_sprout_offered_battlefly_shiny_status(user_id):
                sprout_battlefly = "(Shiny) " + sprout_battlefly
            sprout_price = self.event.get_sprout_requested_battlefly(user_id)
            msg = (f"{ctx.message.author.mention},"
                   " **The Sprout** wants to trade their **{}** for a **{}**"
                   "".format(
                    sprout_battlefly.title(),
                    sprout_price.title()
                    ))
            return msg
        except TheSproutSaleAlreadyMadeException:
            raise
        except Exception as e:
            msg = "Error has occurred in building The Sprout’s offer message."
            self.post_error_log_msg(TheSproutLogicException.__name__, msg, e)
            raise

    def _create_sprout_offer(self, user_id: str):
        """
        Creates an offer from The Sprout to trade
        """
        try:
            offer_battlefly = self.generator.generate_random_battlefly(
                is_sprout_generated=True
            )
            random_battlefly_req = self.generator.generate_random_battlefly()
            sprout_offer = {
                "offer": {
                    "battlefly": offer_battlefly.name,
                    "is_shiny": offer_battlefly.is_shiny
                },
                "price": random_battlefly_req.name
            }
            self.event.update_sprout_offer(user_id, sprout_offer)
        except Exception as e:
            msg = "Error has occurred in creating The Sprout’s offer."
            self.post_error_log_msg(TheSproutLogicException.__name__, msg, e)
            raise

    def reroll_sprout_offer(
        self,
        ctx: discord.ext.commands.Context
    ) -> None:
        """
        Rerolls what The Sprout has to offer to the Ally
        """
        try:
            user_id = get_ctx_user_id(ctx)
            if self.event.check_user_traded(user_id):
                raise TheSproutSaleAlreadyMadeException()
            roll_count = self.event.get_ally_roll_count(user_id)
            if roll_count < 1:
                raise NotEnoughRerollsException()
            self.event.create_or_update_roll_count(user_id)
            self._create_sprout_offer(user_id)
        except TheSproutSaleAlreadyMadeException:
            raise
        except NotEnoughRerollsException:
            raise
        except Exception as e:
            msg = "Error has occurred in rerolling The Sprout’s offer message."
            self.post_error_log_msg(TheSproutLogicException.__name__, msg, e)
            raise

    async def trade_sprout(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Completes a trade with The Sprout
        """
        try:
            user_id = get_ctx_user_id(ctx)
            if not self.event.check_user_has_offer(user_id):
                self.event.create_or_update_roll_count(user_id)
                self._create_sprout_offer(user_id)
            if self.event.check_user_traded(user_id):
                raise TheSproutSaleAlreadyMadeException()
            sprout_battlefly_name = self.event.get_sprout_offered_battlefly(user_id)
            is_sprout_battlefly_shiny = self.event.get_sprout_offered_battlefly_shiny_status(user_id)
            sprout_battlefly = self.assets.get_battlefly_asset(
                sprout_battlefly_name,
                is_sprout_battlefly_shiny
            )
            sprout_price = self.event.get_sprout_requested_battlefly(user_id)
            try:
                await self.release_battlefly_action.release_battlefly(
                    user_id,
                    sprout_price,
                    1
                )
            except HigherReleaseQuantitySpecifiedException:
                raise UnavailableBattleflyToTradeException(
                    sprout_price
                )
            self.ally_service.give_battlefly_to_ally(
                user_id,
                sprout_battlefly
            )
            self.ally_service.save_all_ally_data()
            self.event.update_sprout_sales(user_id)
            formatted_offered_battlefly_name = sprout_battlefly.name.title()
            if is_sprout_battlefly_shiny:
                formatted_offered_battlefly_name = "(Shiny) " + formatted_offered_battlefly_name
            formatted_price_battlefly_name = sprout_price.title()
            msg = (f"{ctx.message.author.mention} traded a"
                   f" **{formatted_offered_battlefly_name}** for a"
                   f" **{formatted_price_battlefly_name}**!")
            return msg
        except TheSproutSaleAlreadyMadeException:
            raise
        except UnavailableBattleflyToTradeException:
            raise
        except Exception as e:
            msg = "Error has occurred in trading with The Sprout."
            self.post_error_log_msg(TheSproutLogicException.__name__, msg, e)
            raise
