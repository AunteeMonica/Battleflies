from modules.battleflybot_module import BattleflyBotModule
from modules.battleflybot_exceptions import BattleflyBotStatusException
from modules.services.ally_service import AllyService
import discord


class BattleflyBotStatus(BattleflyBotModule):
    def __init__(self, bot):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.bot = bot
        self.ally_service = AllyService()
        self.total_battlefly_count = self.ally_service.get_all_total_battlefly_caught_count()

    def increase_total_battlefly_count(self, quantity: int):
        """
        Increments the total Battlefly count.
        """
        try:
            self.total_battlefly_count += quantity
        except Exception as e:
            msg = "Failed to increment total Battlefly count."
            self.post_error_log_msg(BattleflyBotStatusException.__name__, msg, e)
            raise

    def decrease_total_battlefly_count(self, quantity: int):
        """
        Decrements the total Battlefly count.
        """
        try:
            self.total_battlefly_count -= quantity
        except Exception as e:
            msg = "Failed to decrement total Battlefly count."
            self.post_error_log_msg(BattleflyBotStatusException.__name__, msg, e)
            raise

    async def update_status(self):
        """Updates the bot's presence status."""
        try:
            game_status = discord.Game(name="Exploring the Wilds for Battleflies!")
            await self.bot.change_presence(activity=game_status)
            print("✅ Status updated successfully!")
        except Exception as e:
            print(f"❌ Error updating status: {e}")
