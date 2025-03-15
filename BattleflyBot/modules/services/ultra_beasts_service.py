from classes import battleflyBotModule
from database import UltraBeastsDAO
from modules.battleflybot_exceptions import UltraBeastsServiceException


class UltraBeastsService(battleflyBotModule):
    def __init__(self) -> None:
        self.ultra_beasts_dao = UltraBeastsDAO()

    def is_battlefly_ultra_beast(self, pkmn_name: str) -> bool:
        """
        Checks to see if the battlefly is an ultra beast
        """
        try:
            if pkmn_name in self.ultra_beasts_dao.get_ultra_beasts():
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in deciding if a battlefly " \
                  "was an ultra beast."
            self.post_error_log_msg(UltraBeastsServiceException.__name__, msg, e)

    def get_list_of_ultra_beasts(self) -> list:
        """
        Returns the list of ultra beasts
        """
        try:
            return self.ultra_beasts_dao.get_ultra_beasts()
        except Exception as e:
            msg = "Error has occurred in getting list of ultra beasts"
            self.post_error_log_msg(
                UltraBeastsServiceException.__name__,
                msg,
                e
            )
            raise
