from abc import ABC, abstractmethod
from bot_logger import logger
import database.events
import discord

SETTINGS_FOLDER_PATH = "settings"
EVENTS_FOLDER_PATH = f"{SETTINGS_FOLDER_PATH}/events"
WILD_SWARM_EVENT_JSON_PATH = f"{EVENTS_FOLDER_PATH}/wild_swarm_event.json"
NIGHT_VENDOR_EVENT_JSON_PATH = f"{EVENTS_FOLDER_PATH}/night_vendor_event.json"

class battleflyBotEvent(ABC):
    """Generic class to setup battleflyBot Events"""

    def __init__(self, bot, event_key: str):
        self.bot = bot
        self.is_active = False
        self.event_data = {}
        self.catch_cooldown_modifier = 1
        self._load_event_data(event_key)
        print(f"Loaded {type(self).__name__}")

    def _load_event_data(self, event_key: str) -> None:
        """Loads the specific event data given the event key"""
        try:
            self.event_data = database.events.EventsDAO().get_event(event_key)
            self.catch_cooldown_modifier = self.event_data.get("catch_cooldown_modifier", 1.0)
        except Exception as e:
            print("ERROR - Exception: {}".format(str(e)))
            logger.error("Exception: {}".format(str(e)))

    async def _send_event_start_msg(self, msg: str) -> None:
        """Sends a message to the channel that an event has started"""
        battlefly_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "event":
                battlefly_channel = channel.id
        battlefly_channel_obj = self.bot.get_channel(battlefly_channel)
        em = discord.Embed(title="Event Started",
                           description=msg,
                           colour=0x00FF00)
        await battlefly_channel_obj.send(embed=em)

    async def _send_event_end_msg(self, msg: str):
        """Sends a message to the channel that an event has ended"""
        battlefly_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "event":
                battlefly_channel = channel.id
        battlefly_channel_obj = self.bot.get_channel(battlefly_channel)
        em = discord.Embed(title="Event Ended",
                           description=msg,
                           colour=0xFF0000)
        await battlefly_channel_obj.send(embed=em)

    def get_active_state(self) -> bool:
        """Returns event's active state"""
        return self.is_active

    def is_event_enabled(self) -> bool:
        """Returns whether the event is enabled or not"""
        return self.event_data["is_event_enabled"]

    async def process_event_activation_time(self, hour: int) -> None:
        """Checks across all events to see if it's time to activate or deactivate"""
        if not self.is_active:
            if hour == self.event_data["event_start_hour"]:
                await self.activate()
        else:
            if hour == self.event_data["event_end_hour"]:
                await self.deactivate()

    @abstractmethod
    async def activate(self) -> None:
        """Activates the event (to-be-implemented by child)"""

    @abstractmethod
    async def deactivate(self) -> None:
        """Deactivates the event (to-be-implemented by child)"""
