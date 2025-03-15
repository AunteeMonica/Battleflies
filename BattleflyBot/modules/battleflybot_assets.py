from collections import defaultdict
from classes import battleflyBotModule, battlefly
from database import battleflyballsDAO
from modules.services.legendary_battlefly_service import LegendarybattleflyService
from modules.battleflybot_exceptions import (
    battleflyBotAssetsException,
    battleflyDoesNotExistException
)
from modules.services.ultra_beasts_service import UltraBeastsService
import glob
import os
import random
import re


class battleflyBotAssets(battleflyBotModule):
    """
    Handles all battlefly related assets
    """

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    SHINY_PREFIX = "(shiny)"

    def __init__(self):
        self.legendary_service = LegendarybattleflyService()
        self.nrml_battlefly = self._load_battlefly_imgs("nrml")
        self.battleflyballs = battleflyballsDAO()
        self.shiny_battlefly = self._load_battlefly_imgs("shiny")
        self.ultra_service = UltraBeastsService()
        self.bronze_lootbox_battlefly = self._load_bronze_lootbox_battlefly()
        self.silver_lootbox_battlefly = self._load_silver_lootbox_battlefly()
        self.gold_lootbox_battlefly = self._load_gold_lootbox_battlefly()

    def _load_bronze_lootbox_battlefly(self) -> set:
        """
        Loads the pool of bronze lootbox battlefly
        """
        try:
            bronze_lootbox_battlefly = set(self.nrml_battlefly.keys())
            legendary_pkmn = \
                self.legendary_service.get_list_of_legendary_battlefly()
            ultra_beasts = \
                self.ultra_service.get_list_of_ultra_beasts()
            for pkmn in legendary_pkmn:
                bronze_lootbox_battlefly.remove(pkmn)
            for beast in ultra_beasts:
                bronze_lootbox_battlefly.remove(beast)
            return bronze_lootbox_battlefly
        except Exception as e:
            msg = "Error has occurred loading bronze lootbox battlefly."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def _load_silver_lootbox_battlefly(self) -> set:
        """
        Loads the pool of silver lootbox battlefly
        """
        try:
            silver_lootbox_battlefly = set(self.nrml_battlefly.keys())
            return silver_lootbox_battlefly
        except Exception as e:
            msg = "Error has occurred loading silver lootbox battlefly."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def _load_gold_lootbox_battlefly(self) -> set:
        """
        Loads the pool of gold lootbox battlefly
        """
        try:
            legendary_pkmn = \
                self.legendary_service.get_list_of_legendary_battlefly()
            ultra_beasts = \
                self.ultra_service.get_list_of_ultra_beasts()
            gold_lootbox_battlefly = set(legendary_pkmn).union(set(ultra_beasts))
            return gold_lootbox_battlefly
        except Exception as e:
            msg = "Error has occurred loading gold lootbox battlefly."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def _load_battlefly_imgs(self, pkmn_type: str) -> defaultdict:
        """
        Loads battlefly images within a folder

        Note: Make path universal
        """
        try:
            filedict = defaultdict(list)
            folder_path = os.path.join('assets', pkmn_type)
            img_path = os.path.join('assets', pkmn_type, '*.png')
            for filename in glob.glob(img_path):
                result = re.match(r'([^\d]+)', filename)
                if result:
                    pkmn_name = filename.lower()
                    pkmn_name = pkmn_name.replace(folder_path, "")
                    pkmn_name = pkmn_name.replace('/', "")
                    pkmn_name = pkmn_name.replace('\\', "")
                    pkmn_name = pkmn_name.replace('.png', "")
                    filedict[pkmn_name].append(filename)
            return filedict
        except Exception as e:
            msg = "Error has occurred loading battlefly images."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def get_random_battleflyball_emoji(self) -> str:
        """
        Gets a random battleflyball emoji to use in battlefly capture msg
        """
        try:
            return self.battleflyballs.get_random_battleflyball_emoji()
        except Exception as e:
            msg = "Error has occurred in getting random battleflyball."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def get_lootbox_battlefly_asset(
        self,
        is_shiny: bool,
        lootbox: str
    ) -> battlefly:
        """
        Gets a random battlefly from the asset folder
        """
        try:
            lootbox_pkmn = set()
            if lootbox == self.BRONZE:
                lootbox_pkmn = self.bronze_lootbox_battlefly
            elif lootbox == self.SILVER:
                lootbox_pkmn = self.silver_lootbox_battlefly
            elif lootbox == self.GOLD:
                lootbox_pkmn = self.gold_lootbox_battlefly
            pkmn_name = random.sample(lootbox_pkmn, 1)[0]
            return self.get_battlefly_asset(pkmn_name, is_shiny)
        except Exception as e:
            msg = "Error has occurred in getting random battlefly asset."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def get_random_battlefly_asset(self, is_shiny: bool = False) -> battlefly:
        """
        Gets a random battlefly from the asset folder
        """
        try:
            is_egg = False
            if is_shiny:
                random_pkmn = random.choice(list(self.shiny_battlefly.keys()))
                pkmn_img_path = self.shiny_battlefly[random_pkmn][0]
            else:
                random_pkmn = random.choice(list(self.nrml_battlefly.keys()))
                pkmn_img_path = self.nrml_battlefly[random_pkmn][0]
            if random_pkmn == "egg" or random_pkmn == "egg-manaphy":
                is_egg = True
            is_legendary = \
                self.legendary_service.is_battlefly_legendary(random_pkmn)
            is_ultra_beast = \
                self.ultra_service.is_battlefly_ultra_beast(random_pkmn)
            return battlefly(
                name=random_pkmn,
                img_path=pkmn_img_path,
                is_egg=is_egg,
                is_legendary=is_legendary,
                is_shiny=is_shiny,
                is_ultra_beast=is_ultra_beast,
            )
        except Exception as e:
            msg = "Error has occurred in getting random battlefly asset."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise

    def get_battlefly_asset(
        self,
        pkmn_name: str,
        is_shiny: bool = False
    ) -> battlefly:
        """
        Gets a specific battlefly from the asset folder
        """
        try:
            is_egg = False
            if is_shiny:
                pkmn_img_path = self.shiny_battlefly[pkmn_name][0]
            else:
                pkmn_img_path = self.nrml_battlefly[pkmn_name][0]
            if pkmn_name == "egg" or pkmn_name == "egg-manaphy":
                is_egg = True
            is_legendary = \
                self.legendary_service.is_battlefly_legendary(pkmn_name)
            is_ultra_beast = \
                self.ultra_service.is_battlefly_ultra_beast(pkmn_name)
            return battlefly(
                name=pkmn_name,
                img_path=pkmn_img_path,
                is_egg=is_egg,
                is_legendary=is_legendary,
                is_shiny=is_shiny,
                is_ultra_beast=is_ultra_beast,
            )
        except KeyError:
            raise battleflyDoesNotExistException(pkmn_name)
        except Exception as e:
            msg = "Error has occurred in getting specified battlefly asset."
            self.post_error_log_msg(battleflyBotAssetsException.__name__, msg, e)
            raise
