from classes import DataDAO

GIFT_JSON_NAME = "gift.json"

class GiftDAO(DataDAO):
    """
    Gets the available gifts to receive
    from BattleflyBot as well as the gift
    availability state.
    """
    def __init__(self, filename=GIFT_JSON_NAME):
        if getattr(self, "__initialized", False):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GiftDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_gift_list_battlefly(self) -> dict:
        """
        Gets the list of gifted Battleflies to receive from BattleflyBot.
        """
        return self.data["gift_list"]["battlefly"]

    def get_gift_list_cocoon(self) -> dict:
        """
        Gets the list of gifted cocoons to receive from BattleflyBot.
        """
        return self.data["gift_list"]["cocoon"]

    def get_gift_availability(self) -> bool:
        """
        Gets the state of whether allies can
        receive a gift or not.
        """
        return self.data["is_gift_available"]
