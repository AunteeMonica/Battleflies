from classes import DataDAO


LEGENDARY_JSON_NAME = "legendary_pkmn.json"


class LegendarybattleflyDAO(DataDAO):
    """
    Accesses the list of known legendary battlefly
    """
    def __init__(self, filename=LEGENDARY_JSON_NAME):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LegendarybattleflyDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_legendary_battlefly(self) -> list:
        """
        Gets the list of legendary battlefly
        """
        return self.data
