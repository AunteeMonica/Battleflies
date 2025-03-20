from modules.battleflybot_module import BattleflyBotModule
from modules.services.ally_service import AllyService
import discord


class InventoryLogic(BattleflyBotModule):
    """Handles the basic logic of features for BattleflyBot"""

    def __init__(self, bot):
        self.bot = bot
        self.ally_service = AllyService()

    async def display_cocoon_inventory(self, ctx: discord.ext.commands.Context) -> discord.Embed:
        """
        Displays the Ally's cocoon inventory.
        """
        try:
            user_id = ctx.message.author.id
            username = ctx.message.author.name

            cocoon_inventory = self.ally_service.get_entire_cocoon_inventory(user_id)
            msg = '\n'.join([f"**{cocoon.title()}:** {count}" for cocoon, count in cocoon_inventory.items()])

            return discord.Embed(title=f"{username}'s Cocoons", description=msg, colour=0xFF9900)
        except Exception as e:
            msg = "Error has occurred in displaying cocoon inventory"
            self.post_error_log_msg("InventoryLogicException", msg, e)
            raise
