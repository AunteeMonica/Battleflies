from modules.battleflybot_module import BattleflyBotModule
from database import AllyDAO
from modules.battleflybot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    AllyServiceException,
    UnregisteredAllyException
)
from modules.battleflybot_rates import BattleflyBotRates
import discord
import time


class AllyService(BattleflyBotModule):

    def __init__(self, rates: BattleflyBotRates):
        self.ally_dao = AllyDAO()
        self.rates = rates

    def give_battlefly_to_ally(self, user_id: str, battlefly) -> None:
        """
        Gives a Battlefly to the Ally's inventory.
        """
        try:
            self._check_and_create_new_ally(user_id)
            battlefly_name = battlefly.name
            self.ally_dao.increment_battlefly_quantity(user_id, battlefly_name)
        except Exception as e:
            msg = "Error occurred while adding a Battlefly to an Ally."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    def _check_and_create_new_ally(self, user_id: str) -> None:
        """
        Checks if an Ally profile exists; if not, creates one.
        """
        try:
            if not self.ally_dao.is_existing_ally(user_id):
                self.ally_dao.generate_new_ally(user_id)
        except Exception as e:
            msg = "Error occurred while checking/creating Ally profile."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    def get_pollen_shards(self, user_id: str) -> int:
        """
        Retrieves the number of Pollen Shards an Ally has.
        """
        try:
            return self.ally_dao.get_pollen_shards(user_id)
        except Exception as e:
            msg = "Error occurred while retrieving Pollen Shard count."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    def set_pollen_shards_amount(self, user_id: str, pollen_shards: int) -> None:
        """
        Sets the amount of Pollen Shards an Ally has.
        """
        try:
            self.ally_dao.set_pollen_shards(user_id, pollen_shards)
        except Exception as e:
            msg = "Error occurred while updating Pollen Shards."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    def give_cocoon_to_ally(self, user_id: str, cocoon: str) -> None:
        """
        Adds a Cocoon to the Ally's inventory.
        """
        try:
            self._check_and_create_new_ally(user_id)
            self.ally_dao.increment_cocoon_quantity(user_id, cocoon)
        except Exception as e:
            msg = "Error occurred while giving a Cocoon to an Ally."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    def get_cocoon_quantity(self, user_id: str, cocoon: str) -> int:
        """
        Retrieves the number of Cocoons of a specific type in an Ally's inventory.
        """
        try:
            return self.ally_dao.get_cocoon_quantity(user_id, cocoon)
        except Exception as e:
            msg = "Error occurred while retrieving Cocoon quantity."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    def get_all_total_battlefly_caught_count(self) -> int:
        """
        Gets the total number of Battleflies caught by all Allies.
        """
        try:
            return self.ally_dao.get_total_battlefly_caught()
        except Exception as e:
            msg = "Error occurred while retrieving total Battlefly caught count."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise

    async def display_ally_profile(self, user_obj: discord.User) -> discord.Embed:
        """
        Retrieves and displays an Ally's profile.
        """
        try:
            user_id = str(user_obj.id)
            if not self.ally_dao.is_existing_ally(user_id):
                raise UnregisteredAllyException()
            total_battlefly_count = self.ally_dao.get_total_battlefly_count(user_id)
            em = discord.Embed()
            em.set_author(name=user_obj)
            em.set_thumbnail(url=user_obj.avatar)
            em.add_field(name="Total Battleflies Caught", value=total_battlefly_count)
            return em
        except UnregisteredAllyException:
            raise
        except Exception as e:
            msg = "Error occurred while displaying Ally profile."
            self.post_error_log_msg(AllyServiceException.__name__, msg, e)
            raise
