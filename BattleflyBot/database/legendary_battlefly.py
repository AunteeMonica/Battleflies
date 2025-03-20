from classes import DataDAO

LEGENDARY_JSON_NAME = "legendary_battleflies.json"

class LegendaryBattleflyDAO(DataDAO):
    """
    Accesses the list of known Legendary Battleflies.
    """
    def __init__(self, filename=LEGENDARY_JSON_NAME):
        if getattr(self, "__initialized", False):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LegendaryBattleflyDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_legendary_battleflies(self) -> list:
        """
        Gets the list of Legendary Battleflies.
        """
        return self.data
