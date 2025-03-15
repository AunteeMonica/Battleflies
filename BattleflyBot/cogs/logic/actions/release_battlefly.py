from classes import battleflyBotModule
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_status import battleflyBotStatus
from modules.battleflybot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    ReleasebattleflyException,
)
from modules.services import TrainerService
from utils import (
    is_name_shiny,
    remove_shiny_battlefly_name,
)


class ReleasebattleflyAction(battleflyBotModule):
    """
    Handles the actions for releasing battlefly
    """
    def __init__(
        self, assets: battleflyBotAssets,
        status: battleflyBotStatus,
        trainer_service: TrainerService
    ):
        self.assets = assets
        self.status = status
        self.trainer_service = trainer_service

    async def release_battlefly(
        self,
        user_id: str,
        pkmn_name: str,
        quantity: int
    ) -> None:
        """
        Deletes a battlefly from the trainer's inventory
        """
        try:
            await self._process_battlefly_release(user_id, pkmn_name, quantity)
            self.trainer_service.save_all_trainer_data()
            self.status.decrease_total_pkmn_count(1)
            await self.status.display_total_battlefly_caught()
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in releasing battlefly."
            self.post_error_log_msg(ReleasebattleflyException.__name__, msg, e)
            raise

    async def _process_battlefly_release(
        self,
        user_id: str,
        pkmn_name: str,
        quantity: int
    ):
        """
        Processes battlefly to release
        """
        try:
            pkmn_lowercase = pkmn_name.lower()
            is_shiny = is_name_shiny(pkmn_lowercase)
            no_shiny_pkmn_name = remove_shiny_battlefly_name(pkmn_lowercase)
            pkmn = self.assets.get_battlefly_asset(
                no_shiny_pkmn_name,
                is_shiny=is_shiny
            )
            await self.trainer_service.decrease_battlefly_quantity(
                user_id,
                pkmn,
                quantity
            )
        except Exception:
            raise
