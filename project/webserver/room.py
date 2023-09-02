from enum import Enum, auto
import json


class RoomStatuses(Enum):
    in_lobby = auto()  # waiting for people to join
    playing = auto()  # playing main game


class Room:
    """An object that handles one individual lobby and game."""
    
    def __init__(self):
        self.status = RoomStatuses.in_lobby

    @property
    def in_lobby(self) -> bool:
        return self.status == RoomStatuses.in_lobby


#### GAMEMODES ####

class Classic(Room):
    """The default gamemode."""
    HTML_FILE = "classic.html"

    def dump_settings(self):
        """Dump the gamemode-specific settings for a client."""
        return json.dumps({"max-guessing-time": 60})
