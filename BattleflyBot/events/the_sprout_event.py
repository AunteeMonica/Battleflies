from modules.battleflybot_event import BattleflyBotEvent


class TheSproutEvent(BattleflyBotEvent):
    def __init__(self, bot):
        super().__init__(bot, "the_sprout_event")
        self.roll_counts = {}
        self.offers = {}
        self.sales = set()

    async def activate(self):
        """
        Activates The Sprout event
        """
        if not self.is_active:
            self.is_active = True
            msg = ("🌱 **The Sprout has appeared! Use `{0}sprout` to see what it's offering."
                   " If you're interested, type `{0}sprouttrade` to make the trade."
                   " If you don't like the offer, type `{0}sproutroll` to re-roll.**"
                   "".format(self.bot.command_prefix))
            await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates The Sprout event
        """
        self.is_active = False
        self.roll_counts.clear()
        self.offers.clear()
        self.sales.clear()
        msg = "🌱 **The Sprout has disappeared into the wild.**"
        await self._send_event_end_msg(msg)

    def check_user_has_offer(self, user_id: str) -> bool:
        """
        Checks if the Ally has an offer from The Sprout
        """
        return user_id in self.offers

    def check_user_traded(self, user_id: str) -> bool:
        """
        Checks if the Ally has already made a trade
        """
        return user_id in self.sales

    def get_reroll_count(self) -> int:
        """
        Gets the reroll count for The Sprout event
        """
        return self.event_data["reroll_count"]

    def get_sprout_offered_battlefly(self, user_id: str) -> str:
        """
        Gets the offered Battlefly from The Sprout
        """
        return self.offers[user_id]["offer"]

    def get_sprout_requested_battlefly(self, user_id: str) -> str:
        """
        Gets The Sprout's requested Battlefly
        """
        return self.offers[user_id]["price"]

    def get_ally_roll_count(self, user_id: str) -> int:
        """
        Gets the roll count for an Ally
        """
        return self.roll_counts.get(user_id, self.get_reroll_count() + 1)

    def update_sprout_offer(self, user_id: str, sprout_offer: dict) -> None:
        """
        Updates The Sprout's offer for an Ally
        """
        self.offers[user_id] = sprout_offer

    def update_sprout_sales(self, user_id: str) -> None:
        """
        Updates the list of sales completed with The Sprout
        """
        self.sales.add(user_id)

    def create_or_update_roll_count(self, user_id: str):
        """
        Creates or updates the count of rolls for an Ally
        """
        if user_id not in self.roll_counts:
            self.roll_counts[user_id] = self.get_reroll_count()
        else:
            self.roll_counts[user_id] -= 1
