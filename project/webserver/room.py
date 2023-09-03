from enum import Enum, auto
from typing import Protocol


class RoomStatuses(Enum):
    # waiting for people to join
    in_lobby = auto()
    # playing main game
    in_game = auto()


class RoomInterface(Protocol):
    """A standardized interface for handling games."""

    def join(self) -> bool:
        """An interface method for joining the room."""
        ...


#### GAMEMODES ####

class Classic(RoomInterface):
    """The default gamemode."""

    def get_settings(self):
        """Dump the gamemode-specific settings for a client."""
        return {"max-guessing-time": 60}


GAMEMODES = [Classic]
