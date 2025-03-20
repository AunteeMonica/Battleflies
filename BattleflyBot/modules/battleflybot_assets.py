from collections import defaultdict
from modules.battleflybot_module import BattleflyBotModule
from modules.battleflybot_exceptions import (
    BattleflyBotAssetsException,
    BattleflyDoesNotExistException
)
import glob
import os
import random
import re


class BattleflyBotAssets(BattleflyBotModule):
    """
    Handles all Battlefly-related assets.
    """

    def __init__(self):
        self.nrml_battlefly = self._load_battlefly_imgs("nrml")

    def _load_battlefly_imgs(self, battlefly_type: str) -> defaultdict:
        """
        Loads Battlefly images within a folder.
        """
        try:
            filedict = defaultdict(list)
            folder_path = os.path.join('assets', battlefly_type)
            img_path = os.path.join('assets', battlefly_type, '*.png')
            for filename in glob.glob(img_path):
                result = re.match(r'([^\d]+)', filename)
                if result:
                    battlefly_name = filename.lower()
                    battlefly_name = battlefly_name.replace(folder_path, "").replace('/', "").replace('\\', "").replace('.png', "")
                    filedict[battlefly_name].append(filename)
            return filedict
        except Exception as e:
            msg = "Error has occurred loading Battlefly images."
            self.post_error_log_msg(BattleflyBotAssetsException.__name__, msg, e)
            raise

    def get_random_battlefly_asset(self) -> str:
        """
        Gets a random Battlefly from the asset folder.
        """
        try:
            random_battlefly = random.choice(list(self.nrml_battlefly.keys()))
            battlefly_img_path = self.nrml_battlefly[random_battlefly][0]
            return random_battlefly, battlefly_img_path
        except Exception as e:
            msg = "Error has occurred in getting random Battlefly asset."
            self.post_error_log_msg(BattleflyBotAssetsException.__name__, msg, e)
            raise

    def get_battlefly_asset(self, battlefly_name: str) -> str:
        """
        Gets a specific Battlefly from the asset folder.
        """
        try:
            battlefly_img_path = self.nrml_battlefly[battlefly_name][0]
            return battlefly_name, battlefly_img_path
        except KeyError:
            raise BattleflyDoesNotExistException(battlefly_name)
        except Exception as e:
            msg = "Error has occurred in getting specified Battlefly asset."
            self.post_error_log_msg(BattleflyBotAssetsException.__name__, msg, e)
            raise
