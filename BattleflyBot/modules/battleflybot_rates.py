from modules.battleflybot_module import BattleflyBotModule
from database import DailyShopDAO, GeneralRatesDAO, CocoonConfigsDAO
from events import EventManager
from modules.battleflybot_exceptions import BattleflyBotRatesException


class BattleflyBotRates(BattleflyBotModule):
    """Holds the values of the BattleflyBot rates to use and
    allows event-based modifications to the rates.
    """

    def __init__(self, bot):
        self.event_manager = EventManager(bot)
        self.daily_shop_rates = DailyShopDAO()
        self.general_rates = GeneralRatesDAO()
        self.cocoon_rates = CocoonConfigsDAO()

    def get_daily_redemption_reset_hour(self) -> int:
        """
        Gets the hour when the Daily Shop resets for Pollen Shard purchases.
        """
        try:
            return self.daily_shop_rates.get_daily_redemption_reset_hour()
        except Exception as e:
            msg = "Error has occurred getting daily redemption hour."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_daily_shop_menu(self) -> dict:
        """
        Gets the Daily Shop menu for items that can be purchased with Pollen Shards.
        """
        try:
            return self.daily_shop_rates.get_daily_shop_menu()
        except Exception as e:
            msg = "Error has occurred getting daily shop menu."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_catch_cooldown_seconds(self) -> int:
        """
        Gets the catch cooldown applied with any event modifications.
        """
        try:
            return self.general_rates.get_catch_cooldown_seconds() \
                * self.event_manager.get_current_event_catch_cooldown_modifier()
        except Exception as e:
            msg = "Error has occurred getting catch cooldown seconds."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_cocoon_battlefly_limit(self) -> int:
        """
        Gets the number of Battleflies that a Cocoon opening can provide.
        """
        try:
            return self.cocoon_rates.get_cocoon_battlefly_limit()
        except Exception as e:
            msg = "Error has occurred getting Cocoon Battlefly limit."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_daily_cocoon_amber_rate(self) -> float:
        """
        Gets the max probability threshold for an Amber Cocoon 
        given by the Daily Shop or catching a Battlefly.
        """
        try:
            return self.cocoon_rates.get_daily_cocoon_amber_rate()
        except Exception as e:
            msg = "Error has occurred getting daily Amber Cocoon rate."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_daily_cocoon_sapphire_rate(self) -> float:
        """
        Gets the max probability threshold for a Sapphire Cocoon 
        given by the Daily Shop or catching a Battlefly.
        """
        try:
            return self.cocoon_rates.get_daily_cocoon_sapphire_rate()
        except Exception as e:
            msg = "Error has occurred getting daily Sapphire Cocoon rate."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_daily_cocoon_diamond_rate(self) -> float:
        """
        Gets the max probability threshold for a Diamond Cocoon 
        given by the Daily Shop or catching a Battlefly.
        """
        try:
            return self.cocoon_rates.get_daily_cocoon_diamond_rate()
        except Exception as e:
            msg = "Error has occurred getting daily Diamond Cocoon rate."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_cocoon_amber_rate(self) -> float:
        """
        Gets the probability threshold for an Amber Cocoon when catching a Battlefly.
        """
        try:
            return self.cocoon_rates.get_cocoon_amber_rate()
        except Exception as e:
            msg = "Error has occurred getting Amber Cocoon rate."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_cocoon_sapphire_rate(self) -> float:
        """
        Gets the probability threshold for a Sapphire Cocoon when catching a Battlefly.
        """
        try:
            return self.cocoon_rates.get_cocoon_sapphire_rate()
        except Exception as e:
            msg = "Error has occurred getting Sapphire Cocoon rate."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)

    def get_cocoon_diamond_rate(self) -> float:
        """
        Gets the probability threshold for a Diamond Cocoon when catching a Battlefly.
        """
        try:
            return self.cocoon_rates.get_cocoon_diamond_rate()
        except Exception as e:
            msg = "Error has occurred getting Diamond Cocoon rate."
            self.post_error_log_msg(BattleflyBotRatesException.__name__, msg, e)
