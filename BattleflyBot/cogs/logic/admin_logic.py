from modules.battleflybot_module import BattleflyBotModule
from cogs.logic.actions.release_battlefly import ReleasebattleflyAction
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_exceptions import (
    AdminLogicException,
    HigherReleaseQuantitySpecifiedException,
    CocoonDoesNotExistException,
    NotEnoughCocoonQuantityException,
    BattleflyDoesNotExistException,
    UnregisteredAllyException,
)
from modules.battleflybot_rates import battleflyBotRates
from modules.battleflybot_status import battleflyBotStatus
from modules.services.ally_service import AllyService


class AdminLogic(BattleflyBotModule):
    """
    Handles logic related to admin commands
    """

    # TODO: Keep this value in a constants file for global use
    COCOONS_AVAILABLE = ["bronze", "silver", "gold"]

    def __init__(self, bot):
        self.assets = battleflyBotAssets()
        self.rates = battleflyBotRates(bot)
        self.status = battleflyBotStatus(bot)
        self.ally_service = AllyService(self.rates)
        self.release_battlefly = ReleasebattleflyAction(
            self.assets,
            self.status,
            self.ally_service
        )

    async def give_battlefly(
        self,
        user_id: str,
        battlefly_name: str,
        is_shiny=False
    ) -> None:
        """
        Gives a Battlefly to the Ally
        """
        try:
            battlefly = self.assets.get_battlefly_asset(battlefly_name, is_shiny)
            self.ally_service.give_battlefly_to_ally(
                user_id,
                battlefly,
            )
            self.status.increase_total_battlefly_count(1)
            await self.status.display_total_battlefly_caught()
            self.ally_service.save_all_ally_data()
        except BattleflyDoesNotExistException:
            raise
        except Exception as e:
            msg = "Error has occurred in giving Battlefly to Ally."
            self.post_error_log_msg(AdminLogicEx)
