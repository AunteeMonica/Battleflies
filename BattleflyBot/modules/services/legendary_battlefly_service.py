from modules.battleflybot_module import BattleflyBotModule
from database import LegendaryBattleflyDAO
from modules.battleflybot_exceptions import LegendaryBattleflyServiceException


class LegendaryBattleflyService(BattleflyBotModule):
    """
    Handles logic related to Legendary Battleflies.
    """

    def __init__(self) -> None:
        self.legendary_dao = LegendaryBattleflyDAO()

    def is_battlefly_legendary(self, battlefly_name: str) -> bool:
        """
        Checks if the given Battlefly is a Legendary Battlefly.
        """
        try:
            return battlefly_name in self.legendary_dao.get_legendary_battlefly()
        except Exception as e:
            msg = "Error has occurred while checking if a Battlefly is legendary."
            self.post_error_log_msg(LegendaryBattleflyServiceException.__name__, msg, e)
            raise

    def get_list_of_legendary_battleflies(self) -> list:
        """
        Returns the list of all Legendary Battleflies.
        """
        try:
            return self.legendary_dao.get_legendary_battlefly()
        except Exception as e:
            msg = "Error has occurred while retrieving the list of Legendary Battleflies."
            self.post_error_log_msg(LegendaryBattleflyServiceException.__name__, msg, e)
            raise
