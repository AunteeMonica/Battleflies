from classes import battleflyBotModule
from database import LegendarybattleflyDAO
from modules.battleflybot_exceptions import LegendarybattleflyServiceException


class LegendarybattleflyService(battleflyBotModule):
    def __init__(self) -> None:
        self.legendary_dao = LegendarybattleflyDAO()

    def is_battlefly_legendary(self, pkmn_name: str) -> bool:
        """
        Gives the battlefly to the trainer in their inventory
        """
        try:
            if pkmn_name in self.legendary_dao.get_legendary_battlefly():
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in deciding if a battlefly " \
                  "was a legendary battlefly."
            self.post_error_log_msg(
                LegendarybattleflyServiceException.__name__,
                msg,
                e
            )
            raise

    def get_list_of_legendary_battlefly(self) -> list:
        """
        Returns the list of legendary battlefly
        """
        try:
            return self.legendary_dao.get_legendary_battlefly()
        except Exception as e:
            msg = "Error has occurred in getting list of legendary battlefly"
            self.post_error_log_msg(
                LegendarybattleflyServiceException.__name__,
                msg,
                e
            )
            raise
