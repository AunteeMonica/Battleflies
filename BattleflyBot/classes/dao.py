import json
import os

DATA_FOLDER_PATH = "data"
CONFIG_FOLDER_PATH = f"{DATA_FOLDER_PATH}/configs"

class JSONDAO:
    """
    Generic class for loading and saving JSON files
    related to BattleflyBot.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_json()

    def _load_json(self):
        """Loads JSON data, or creates an empty file if missing."""
        if not os.path.exists(self.file_path):
            print(f"⚠️ Warning: {self.file_path} not found. Creating a new file.")
            self._save_json({})
        try:
            with open(self.file_path, "r", encoding="utf-8") as jsonfile:
                return json.load(jsonfile)
        except json.JSONDecodeError:
            print(f"❌ Error: Corrupt JSON in {self.file_path}. Resetting.")
            self._save_json({})
            return {}

    def _save_json(self, data):
        """Safely writes data to JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=2)

    def save(self):
        """Public method to save current data."""
        self._save_json(self.data)


class ConfigDAO(JSONDAO):
    """
    Loads config JSON files from the configs folder.
    """
    def __init__(self, file_name):
        super().__init__(f"{CONFIG_FOLDER_PATH}/{file_name}")


class DataDAO(JSONDAO):
    """
    Loads general data JSON files from the data folder.
    """
    def __init__(self, file_name):
        super().__init__(f"{DATA_FOLDER_PATH}/{file_name}")
