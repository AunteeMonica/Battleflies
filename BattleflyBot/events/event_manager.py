from modules.battleflybot_event import BattleflyBotEvent
from events.wild_swarm_event import WildSwarmEvent
from events.the_sprout_event import TheSproutEvent
import datetime


class EventManager(object):

    WILD_SWARM_KEY = "wild_swarm"
    THE_SPROUT_KEY = "the_sprout"

    def __init__(self, bot):
        if (self.__initialized):
            return
        self.__initialized = True
        self.active_events = {}
        self.events = {
            self.WILD_SWARM_KEY: WildSwarmEvent(bot),
            self.THE_SPROUT_KEY: TheSproutEvent(bot),
        }
        self.event_catch_cooldown_modifier = 1.0

    def __new__(*args):
        cls = args[0]
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventManager, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def _get_all_events(self) -> list:
        return self.events

    def is_event_active(self, event_key: str) -> bool:
        """
        Checks to see if an event is active
        """
        return self.events[event_key].get_active_state()

    def get_event_by_key(self, event_key: str) -> BattleflyBotEvent:
        """
        Returns the BattleflyBotEvent object given the event key
        """
        return self.events[event_key]

    def get_current_event_catch_cooldown_modifier(self) -> float:
        return self.event_catch_cooldown_modifier

    async def process_all_event_activation_times(self) -> None:
        """
        Iterate through each event to determine activation and apply side effects.
        Wild Swarm triggers every 333 minutes.
        """
        for event_key in self.events:
            event = self.events[event_key]
            if event.is_event_enabled():
                await event.activate()
                await self._set_event_side_effects(event)

    async def _set_event_side_effects(self, event) -> None:
        """
        Sets the side effects that occur from active/inactive events
        """
        if event.is_active:
            if type(event).__name__ not in self.active_events:
                self.active_events[type(event).__name__] = True
                self.event_catch_cooldown_modifier *= event.catch_cooldown_modifier
        else:
            if type(event).__name__ in self.active_events:
                self.active_events[type(event).__name__] = False
                self.event_catch_cooldown_modifier /= event.catch_cooldown_modifier
