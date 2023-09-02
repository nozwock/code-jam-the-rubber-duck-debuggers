from enum import Enum, auto

class RoomStatuses:
  in_lobby = auto() # waiting for people to join
  playing = auto() # playing main game

class Room:
  def __init__(self):
    self.status = in_lobby

  @property
  def in_lobby(self) -> bool:
    return self.status == RoomStatuses.in_lobby