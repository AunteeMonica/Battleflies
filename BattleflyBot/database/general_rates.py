from classes import ConfigDAO

GENERAL_CONFIG_NAME = "general_config.json"

class GeneralRatesDAO(ConfigDAO):
    """
    Gets the general rate configs for BattleflyBot.
    """
    def __init__(self, filename=GENERAL_CONFIG_NAME):
        if getattr(self, "__initialized", False):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GeneralRatesDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_daily_redemption_reset_hour(self) -> int:
        """
        Gets the hour to reset daily rewards.
        """
        return self.data["daily_redemption_reset_hour"]
