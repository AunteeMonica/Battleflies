from classes import battlefly, battleflyBotModule
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_rates import battleflyBotRates
from modules.battleflybot_exceptions import battleflyBotGeneratorException
import random


class battleflyBotGenerator(battleflyBotModule):

    def __init__(self, assets: battleflyBotAssets, rates: battleflyBotRates):
        self.assets = assets
        self.rates = rates

    def generate_random_battlefly(
        self,
        is_shiny: bool = False,
        is_egg: bool = False,
        is_night_vendor_generated: bool = False,
        lootbox: str = ''
    ) -> battlefly:
        """
        Generates a random battlefly and returns a battlefly object
        """
        try:
            is_shiny_battlefly = is_shiny
            if not is_shiny:
                is_shiny_battlefly = self._determine_shiny_battlefly(
                    is_egg,
                    is_night_vendor_generated
                )
            if lootbox:
                pkmn = self.assets.get_lootbox_battlefly_asset(
                    is_shiny_battlefly,
                    lootbox
                )
            else:
                pkmn = self.assets.get_random_battlefly_asset(
                    is_shiny=is_shiny_battlefly
                )
            return pkmn
        except Exception as e:
            msg = "Error has occurred in generating battlefly."
            self.post_error_log_msg(battleflyBotGeneratorException.__name__, msg, e)
            raise

    def _determine_shiny_battlefly(
        self,
        is_egg: bool,
        is_night_vendor_generated: bool
    ) -> bool:
        """
        Determines the odds of a shiny battlefly
        """
        try:
            shiny_catch_rate = -1
            shiny_rng_chance = random.uniform(0, 1)
            if is_night_vendor_generated:
                shiny_catch_rate = self.rates.get_shiny_pkmn_night_vendor_rate()
            elif is_egg:
                shiny_catch_rate = self.rates.get_shiny_pkmn_hatch_multiplier()
            else:
                shiny_catch_rate = self.rates.get_shiny_pkmn_catch_rate()
            if shiny_rng_chance < shiny_catch_rate:
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in determining shiny battlefly."
            self.post_error_log_msg(battleflyBotGeneratorException.__name__, msg, e)
            raise

    def generate_battlefly(self, pkmn_name: str, is_egg=False) -> battlefly:
        """
        Generates a specified battlefly and returns a battlefly object
        """
        try:
            is_shiny_battlefly = self._determine_shiny_battlefly(is_egg)
            if is_shiny_battlefly:
                pkmn = self.assets.get_battlefly_asset(pkmn_name, is_shiny=True)
            else:
                pkmn = self.assets.get_battlefly_asset(pkmn_name)
            return pkmn
        except Exception as e:
            msg = "Error has occurred in generating specific battlefly."
            self.post_error_log_msg(battleflyBotGeneratorException.__name__, msg, e)
            raise

    def generate_lootbox(self, daily=False) -> str:
        """
        Generates a lootbox with consideration into daily or catch rates
        """
        try:
            lootbox_rng = random.uniform(0, 1)
            if daily:
                lootbox_bronze_rate = \
                    self.rates.get_daily_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.rates.get_daily_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.rates.get_daily_lootbox_gold_rate()
            else:
                lootbox_bronze_rate = \
                    self.rates.get_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.rates.get_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.rates.get_lootbox_gold_rate()
            if lootbox_rng < lootbox_gold_rate:
                return "gold"
            elif lootbox_rng < lootbox_silver_rate:
                return "silver"
            elif lootbox_rng < lootbox_bronze_rate:
                return "bronze"
            return None
        except Exception as e:
            msg = "Error has occurred in generating lootbox."
            self.post_error_log_msg(battleflyBotGeneratorException.__name__, msg, e)
            raise
