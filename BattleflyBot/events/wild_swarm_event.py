import time
from modules.battleflybot_event import BattleflyBotEvent


class WildSwarmEvent(BattleflyBotEvent):
    def __init__(self, bot):
        super().__init__(bot, "wild_swarm_event")
        self.last_activated_time = 0  # Store last activation time

    def is_event_enabled(self) -> bool:
        """
        Determines if the Wild Swarm event should activate.
        Triggers every 333 minutes.
        """
        current_time = time.time()
        minutes_since_last_activation = (current_time - self.last_activated_time) / 60

        if minutes_since_last_activation >= 333:
            self.last_activated_time = current_time
            return True
        return False

    async def activate(self):
        """
        Activates Wild Swarm event
        """
        if not self.is_active:
            self.is_active = True
            msg = ("🐝 **A Wild Swarm has begun! Battleflies are appearing more frequently,"
                   " and the catch cooldown is reduced. Good luck @everyone!**")
            await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates Wild Swarm event
        """
        self.is_active = False
        msg = "🐝 **The Wild Swarm has ended. The Battleflies have settled down.**"
        await self._send_event_end_msg(msg)
