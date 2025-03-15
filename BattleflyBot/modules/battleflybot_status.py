from classes import battleflyBotModule
from modules.battleflybot_exceptions import battleflyBotStatusException
from modules.battleflybot_rates import battleflyBotRates
from modules.services import TrainerService
import discord


class battleflyBotStatus(battleflyBotModule):
    def __init__(self, bot):
        if (self.__initialized):
            return
        self.__initialized = True
        self.bot = bot
        self.rates = battleflyBotRates(bot)
        self.trainer_service = TrainerService(self.rates)
        self.total_battlefly_count = \
            self.trainer_service.get_all_total_battlefly_caught_count()

    def __new__(*args):
        cls = args[0]
        if not hasattr(cls, 'instance'):
            cls.instance = super(battleflyBotStatus, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def increase_total_battlefly_count(self, quantity: int):
        """
        Increments the total battlefly count
        """
        try:
            self.total_battlefly_count += quantity
        except Exception as e:
            msg = "Failed to increment total battlefly count."
            self.post_error_log_msg(battleflyBotStatusException.__name__, msg, e)
            raise

    def decrease_total_battlefly_count(self, quantity: int):
        """
        Decrements the total battlefly count
        """
        try:
            self.total_battlefly_count -= 1
        except Exception as e:
            msg = "Failed to increment total battlefly count."
            self.post_error_log_msg(battleflyBotStatusException.__name__, msg, e)
            raise

class battleflyBotStatus(battleflyBotModule):
    def __init__(self, bot):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.bot = bot
        self.rates = battleflyBotRates(bot)
        self.trainer_service = TrainerService(self.rates)
        self.total_battlefly_count = \
            self.trainer_service.get_all_total_battlefly_caught_count()

    async def update_status(self):
        """Updates the bot's presence status"""
        try:
            game_status = discord.Game(name="Catching Battleflies!")  # Update the status
            await self.bot.change_presence(activity=game_status)
            print("✅ Status updated successfully!")
        except Exception as e:
            print(f"❌ Error updating status: {e}")



