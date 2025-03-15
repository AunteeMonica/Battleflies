from classes import battleflyBotCog
from discord.ext import commands, tasks
from events import EventManager
from modules.battleflybot_status import battleflyBotStatus


class battleflyBotTasks(battleflyBotCog):
    """Runs async tasks for battleflyBot that run in a timely manner"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.event_manager = EventManager(bot)
        self.status = battleflyBotStatus(bot)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        self._process_all_event_activation_times.start()
        await self.status.display_total_battlefly_caught()

    @tasks.loop(seconds=60.0)
    async def _process_all_event_activation_times(self):
        """
        Checks if it's time for an event and activate it
        """
        await self.event_manager.process_all_event_activation_times()
