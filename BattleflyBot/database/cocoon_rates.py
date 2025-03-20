from classes import ConfigDAO

COCOON_CONFIG_NAME = "cocoon_rates_config.json"

class CocoonConfigsDAO(ConfigDAO):
    """
    Gets the configs for cocoons.
    """
    def __init__(self, filename=COCOON_CONFIG_NAME):
        if getattr(self, "__initialized", False):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CocoonConfigsDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_cocoon_battlefly_limit(self) -> int:
        """
        Gets the number of Battleflies that a cocoon
        opening can provide to an ally.
        """
        return self.data["cocoon_battlefly_limit"]

    def get_daily_cocoon_amber_rate(self) -> float:
        """
        Gets the max number threshold for an amber
        cocoon given by the daily token redemption.
        """
        return self.data["daily_cocoon_amber_rate"]

    def get_daily_cocoon_sapphire_rate(self) -> float:
        """
        Gets the max number threshold for a sapphire
        cocoon given by the daily token redemption.
        """
        return self.data["daily_cocoon_sapphire_rate"]

    def get_daily_cocoon_diamond_rate(self) -> float:
        """
        Gets the max number threshold for a diamond
        cocoon given by the daily token redemption.
        """
        return self.data["daily_cocoon_diamond_rate"]

    def get_cocoon_amber_rate(self) -> float:
        """
        Gets the max number threshold for an amber
        cocoon given by catching a Battlefly.
        """
        return self.data["cocoon_amber_rate"]

    def get_cocoon_sapphire_rate(self) -> float:
        """
        Gets the max number threshold for a sapphire
        cocoon given by catching a Battlefly.
        """
        return self.data["cocoon_sapphire_rate"]

    def get_cocoon_diamond_rate(self) -> float:
        """
        Gets the max number threshold for a diamond
        cocoon given by catching a Battlefly.
        """
        return self.data["cocoon_diamond_rate"]
