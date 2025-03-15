from classes import DataDAO
import random


battleflyBALL_JSON_NAME = "battleflyballs.json"


class battleflyballsDAO(DataDAO):
    """
    Gets the list of all battleflyball
    """
    def __init__(self, filename=battleflyBALL_JSON_NAME):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(battleflyballsDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_random_battleflyball_emoji(self) -> str:
        """
        Gets a random battleflyball from the list of battleflyball emojis
        available
        """
        if not self.data:
            return ''
        return random.choice(list(self.data))
