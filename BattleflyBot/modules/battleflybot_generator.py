from modules.battleflybot_module import BattleflyBotModule
from modules.battleflybot_assets import BattleflyBotAssets
from modules.battleflybot_exceptions import BattleflyBotGeneratorException
import random


class BattleflyBotGenerator(BattleflyBotModule):

    def __init__(self, assets: BattleflyBotAssets):
        self.assets = assets

    def generate_random_battlefly(self) -> tuple:
        """
        Generates a random Battlefly and returns its name and image path.
        """
        try:
            return self.assets.get_random_battlefly_asset()
        except Exception as e:
            msg = "Error has occurred in generating Battlefly."
            self.post_error_log_msg(BattleflyBotGeneratorException.__name__, msg, e)
            raise

    def generate_battlefly(self, battlefly_name: str) -> tuple:
        """
        Generates a specified Battlefly and returns its name and image path.
        """
        try:
            return self.assets.get_battlefly_asset(battlefly_name)
        except Exception as e:
            msg = "Error has occurred in generating specific Battlefly."
            self.post_error_log_msg(BattleflyBotGeneratorException.__name__, msg, e)
            raise
