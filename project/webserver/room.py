from enum import Enum, auto


class RoomStatuses(Enum):
    # waiting for people to join
    in_lobby = auto()
    # playing main game
    playing = auto()


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
