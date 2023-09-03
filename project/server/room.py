from enum import Enum, auto
from typing import Protocol, Type


class RoomStatus(Enum):
    LOBBY = auto()
    INGAME = auto()


class RoomInterface(Protocol):
    id: str

    @property
    def in_lobby(self) -> bool:
        """Returns if the players are in the lobby."""
        ...

    @property
    def in_game(self) -> bool:
        """Returns if the game has started already."""
        ...

    def get_settings(self) -> dict:
        """Dump the gamemode-specific settings for a client."""
        ...


#### GAMEMODES ####


class ClassicRoom(RoomInterface):
    """The default gamemode."""

    def __init__(self):
        self.id = "ClassicRoom"
        self.status = RoomStatus.LOBBY

    @property
    def in_lobby(self) -> bool:
        """Returns if the players are in the lobby."""
        return self.status == RoomStatus.LOBBY

    @property
    def in_game(self) -> bool:
        """Returns if the game has started already."""
        return self.status == RoomStatus.INGAME

    def get_settings(self) -> dict:
        """Dump the gamemode-specific settings for a client."""
        return {"max-guessing-time": 60}


GAMEMODES: list[Type[RoomInterface]] = [ClassicRoom]
