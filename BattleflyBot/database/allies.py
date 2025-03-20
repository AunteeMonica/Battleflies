from classes import DataDAO

ALLIES_JSON_FILE = "allies.json"

class AlliesDAO(DataDAO):
    """
    Accesses, modifies, and returns the BattleflyBot JSON data.
    """
    AMBER = "amber"
    SAPPHIRE = "sapphire"
    DIAMOND = "diamond"

    EGG_COUNT = "egg_count"
    BATTLEFLY_INVENTORY = "battleflies"
    LAST_CATCH_TIME = "last_catch_time"
    LAST_DAILY_REDEEMED_TIME = "last_daily_redeemed_time"
    COCOONS = "cocoons"
    POLLEN_SHARDS = "pollen_shards"
    LEGENDARY_BATTLEFLY_COUNT = "legendary_battlefly_count"
    TOTAL_BATTLEFLY_COUNT = "total_battlefly_count"

    def __init__(self, filename=ALLIES_JSON_FILE):
        if getattr(self, "__initialized", False):
            return
        self.__initialized = True
        super().__init__(filename)

    def is_existing_ally(self, user_id: str) -> bool:
        """
        Checks if an ally exists and returns True if so, otherwise False.
        """
        return bool(self.data.get(user_id, False))

    def get_battlefly_inventory(self, user_id: str) -> dict:
        """
        Gets the inventory of Battleflies from the ally.
        """
        return self.data[user_id][self.BATTLEFLY_INVENTORY]

    def get_battlefly_quantity(self, user_id: str, battlefly_name: str) -> int:
        """
        Gets the number of a specific Battlefly from the inventory.
        """
        return self.data[user_id][self.BATTLEFLY_INVENTORY].get(battlefly_name, 0)

    def increment_battlefly_quantity(self, user_id: str, battlefly_name: str) -> None:
        """
        Increments the quantity of a specific ally's Battlefly
        within their inventory.
        """
        inventory = self.get_battlefly_inventory(user_id)
        inventory[battlefly_name] = inventory.get(battlefly_name, 0) + 1

    def get_last_catch_time(self, user_id: str) -> float:
        """
        Gets the last catch time of the ally.
        """
        return self.data[user_id].get(self.LAST_CATCH_TIME, 0)

    def get_last_daily_redeemed_time(self, user_id: str) -> float:
        """
        Gets the last daily redeemed time of the ally.
        """
        return self.data[user_id].get(self.LAST_DAILY_REDEEMED_TIME, 0)

    def get_cocoon_inventory(self, user_id: str) -> dict:
        """
        Gets the inventory of cocoons that the ally has.
        """
        return self.data[user_id][self.COCOONS]

    def increment_cocoon_quantity(self, user_id: str, cocoon) -> None:
        """
        Increments the quantity of the cocoon specified in the ally's inventory.
        """
        self.data[user_id][self.COCOONS][cocoon] += 1

    def get_pollen_shards(self, user_id: str) -> int:
        """
        Gets the number of pollen shards the ally has.
        """
        return self.data[user_id].get(self.POLLEN_SHARDS, 0)

    def set_last_catch_time(self, user_id: str, time: float) -> None:
        """
        Sets the ally's last catch time.
        """
        self.data[user_id][self.LAST_CATCH_TIME] = time

    def set_last_daily_redeemed_time(self, user_id: str, time: float) -> None:
        """
        Sets the ally's last daily redeemed time.
        """
        self.data[user_id][self.LAST_DAILY_REDEEMED_TIME] = time

    def get_total_battlefly_caught(self) -> int:
        """
        Gets the total amount of Battleflies caught across all allies.
        """
        return sum(user_data.get(self.TOTAL_BATTLEFLY_COUNT, 0) for user_data in self.data.values())

    def get_legendary_battlefly_count(self, user_id: str) -> int:
        """
        Gets the legendary Battlefly count.
        """
        return self.data[user_id].get(self.LEGENDARY_BATTLEFLY_COUNT, 0)

    def increment_legendary_battlefly_count(self, user_id: str) -> None:
        """
        Increments the ally's count for legendary Battleflies.
        """
        self.data[user_id][self.LEGENDARY_BATTLEFLY_COUNT] += 1

    def get_egg_count(self, user_id: str) -> int:
        """
        Gets the amount of eggs that exist with the user.
        """
        return self.data[user_id].get(self.EGG_COUNT, 0)

    def increment_egg_count(self, user_id: str) -> None:
        """
        Increments the ally's egg count.
        """
        self.data[user_id][self.EGG_COUNT] += 1

    def decrement_egg_count(self, user_id: str) -> None:
        """
        Decrements the ally's egg count.
        """
        if self.data[user_id][self.EGG_COUNT] > 0:
            self.data[user_id][self.EGG_COUNT] -= 1
