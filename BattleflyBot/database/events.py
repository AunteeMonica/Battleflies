from classes import DataDAO

EVENTS_JSON_NAME = "events.json"

class EventsDAO(DataDAO):
    """
    Manages the list of events available in BattleflyBot.
    """
    def __init__(self, filename=EVENTS_JSON_NAME):
        if getattr(self, "__initialized", False):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventsDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_events(self) -> dict:
        """
        Returns all available events.
        """
        return self.data

    def get_event(self, event_key: str) -> dict:
        """
        Returns data for a specific event.
        If event_key is missing, returns an empty event instead of crashing.
        """
        return self.data.get(event_key, {
            "is_event_enabled": False
        })
