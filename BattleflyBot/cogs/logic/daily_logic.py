from modules.battleflybot_module import BattleflyBotModule
from modules.battleflybot_exceptions import (
    DailyLogicException,
    DailyCooldownIncompleteException,
    ImproperDailyShopItemNumberException,
    NotEnoughDailyShopTokensException
)
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_rates import battleflyBotRates
from modules.battleflybot_status import battleflyBotStatus
from modules.battleflybot_generator import battleflyBotGenerator
from modules.services.ally_service import AllyService
from utils import get_ctx_user_id
import datetime
import discord
import time


class DailyLogic(BattleflyBotModule):
    """
    Handles logic for daily commands
    """

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    SHINY = "shiny"

    ITEM_DESCRIPTION = "description"
    ITEM_PRICE = "price"

    def __init__(self, bot):
        self.assets = battleflyBotAssets()
        self.rates = battleflyBotRates(bot)
        self.status = battleflyBotStatus(bot)
        self.generator = battleflyBotGenerator(self.assets, self.rates)
        self.ally_service = AllyService(self.rates)
        self.daily_shop_menu = self.rates.get_daily_shop_menu()

    def claim_daily(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Claims the daily cocoon for the Ally
        """
        try:
            current_time = time.time()
            user_id = get_ctx_user_id(ctx)
            if not self._check_user_daily_redemption(user_id):
                raise DailyCooldownIncompleteException()
            daily_cocoon = self.generator.generate_cocoon(daily=True)
            self.ally_service.give_cocoon_to_ally(
                user_id,
                daily_cocoon,
            )
            self.ally_service.set_ally_last_daily_redeemed_time(
                user_id,
                current_time
            )
            self.ally_service.increment_ally_daily_token_count(user_id)
            self.ally_service.save_all_ally_data()
            return daily_cocoon.title()
        except DailyCooldownIncompleteException:
            raise
        except Exception as e:
            msg = ("Error has occurred in claiming daily from "
                   f"Ally ({user_id}).")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    def _check_user_daily_redemption(
        self,
        user_id: str
    ) -> bool:
        """
        Checks if the user can use the daily command
        """
        try:
            # get user daily time
            ally_last_daily_redeemed_time = \
                self.ally_service.get_ally_last_daily_redeemed_time(
                    user_id
                )
            datetime_last_daily_redeemed_time = datetime.datetime.fromtimestamp(
                ally_last_daily_redeemed_time
            )
            # get daily claim reset time
            reset_hour = self.rates.get_daily_redemption_reset_hour()
            datetime_reset_hour = datetime.time(reset_hour, 0, 0)
            reset_time = datetime.datetime.combine(
                datetime.date.today(),
                datetime_reset_hour
            )
            if datetime_last_daily_redeemed_time < reset_time:
                return True
            return False
        except Exception as e:
            msg = ("Error has occurred in checking Ally's daily "
                   f"claim ({user_id}).")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    def build_daily_tokens_msg():
        self,
        ctx: discord.ext.commands.Conte
