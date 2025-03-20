from modules.battleflybot_module import BattleflyBotModule
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_status import battleflyBotStatus
from modules.battleflybot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    ReleaseBattleflyException,
)
from modules.services.ally_service import AllyService
from utils import (
    is_name_shiny,
    remove_shiny_battlefly_name,
)


class ReleaseBattleflyAction(BattleflyBotModule):
    """
    Handles the actions for releasing Battleflies
    """
    def __init__(
        self, assets: battleflyBotAssets,
        status: battleflyBotStatus,
        ally_service: AllyService
    ):
        self.assets = assets
        self.status = status
        self.ally_service = ally_service

    async def release_battlefly(
        self,
        user_id: str,
        battlefly_name: str,
        quantity: int
    ) -> None:
        """
        Deletes a Battlefly from the Ally's inventory
        """
        try:
            await self._process_battlefly_release(user_id, battlefly_name, quantity)
            self.ally_service.save_all_ally_data()
            self.status.decrease_total_battlefly_count(1)
            await self.status.display_total_battlefly_caught()
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in releasing Battlefly."
            self.post_error_log_msg(ReleaseBattleflyException.__name__, msg, e)
            raise

    async def _process_battlefly_release(
        self,
        user_id: str,
        battlefly_name: str,
        quantity: int
    ):
        """
        Processes Battlefly release
        """
        try:
            battlefly_lowercase = battlefly_name.lower()
            is_shiny = is_name_shiny(battlefly_lowercase)
            no_shiny_battlefly_name = remove_shiny_battlefly_name(battlefly_lowercase)
            battlefly = self.assets.get_battlefly_asset(
                no_shiny_battlefly_name,
                is_shiny=is_shiny
            )
            await self.ally_service.decrease_battlefly_quantity(
                user_id,
                battlefly,
                quantity
            )
        except Exception:
            raise
