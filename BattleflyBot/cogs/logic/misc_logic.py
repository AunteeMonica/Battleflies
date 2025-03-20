from bot_logger import logger
from modules.battleflybot_module import BattleflyBotModule
from modules.battleflybot_exceptions import (
    MiscLogicException,
    UnregisteredAllyException
)
from modules.battleflybot_rates import battleflyBotRates
from modules.services.ally_service import AllyService
from utils import parse_discord_mention_user_id
import discord


class MiscLogic(BattleflyBotModule):
    """Handles the miscellaneous logic of features for BattleflyBot"""

    def __init__(self, bot):
        self.ally_service = AllyService(battleflyBotRates(bot))

    async def build_gif_embed(
        self,
        battlefly_name: str,
        shiny: str
    ) -> discord.Embed:
        """
        Builds the gif message to display a Battlefly animation.
        """
        try:
            em = discord.Embed()
            if shiny == "shiny" or shiny == "s":
                em.set_image(url="https://play.battleflyshowdown.com/sprites/"
                                 "xyani-shiny/{}.gif"
                                 "".format(battlefly_name))
            else:
                em.set_image(url="https://play.battleflyshowdown.com/sprites/"
                                 "xyani/{}.gif"
                                 "".format(battlefly_name))
            return em
        except MiscLogicException as e:
            print("An error has occurred in displaying a gif. See error.log.")
            logger.error("MiscCommandsException: {}".format(str(e)))

    async def build_ally_profile_msg(
        self,
        ctx: discord.ext.commands.Command,
        user_mention: str
    ) -> discord.Embed:
        """
        Displays Ally profile and Battlefly caught stats.
        """
        try:
            # Discord's 'get_user' API uses int user_id
            # Whereas our JSON file keeps it as a string
            user_id = parse_discord_mention_user_id(user_mention)
            user_obj = ctx.bot.get_user(int(user_id))
            return await self.ally_service.display_ally_profile(user_obj)
        except UnregisteredAllyException:
            raise
