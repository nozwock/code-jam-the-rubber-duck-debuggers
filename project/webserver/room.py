from enum import Enum, auto


class RoomStatuses(Enum):
    in_lobby = auto()  # waiting for people to join
    in_game = auto()  # playing main game


class Room:
    """An object that handles one individual lobby and game."""
    def __init__(self):
        self.status = RoomStatuses.in_lobby

    @property
    def in_lobby(self) -> bool:
        """Returns if the players are in the lobby."""
        return self.status == RoomStatuses.in_lobby

    @property
    def in_game(self) -> bool:
        """Returns if the game has started already."""
        return self.status == RoomStatuses.in_game


#### GAMEMODES ####

class Classic(Room):
    """The default gamemode."""

    def get_settings(self):
        """Dump the gamemode-specific settings for a client."""
        return {"max-guessing-time": 60}


GAMEMODES = [Classic]
