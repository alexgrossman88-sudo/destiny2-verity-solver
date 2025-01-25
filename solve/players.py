from dataclasses import dataclass

from .states.base import PositionsType


@dataclass(slots=True)
class Player:
    """
    An object which holds player's alias.

    Keep mutable to allow updates to the alias.
    This is useful for dynamically changing player's alais
    after all steps are created in cases when someone dies.
    """
    alias: str

    def __format__(self, format_spec: str, /) -> str:
        return format(self.alias, format_spec)


@dataclass(frozen=True, kw_only=True, slots=True)
class AllPlayers:
    """
    All players.

    Immutable, so references to player objects are locked.
    For example,
    whenever a step references the player in the left room,
    that step will continue to reference the player in the left room
    even if original player died and was replaced.
    """
    left: Player
    middle: Player
    right: Player

    dissector: Player
    helper1: Player
    helper2: Player

    def solo_player(self, room_position: PositionsType, /) -> Player:
        """
        Get the solo player inside the given room.
        """
        return getattr(self, room_position)


__all__ = 'Player', 'AllPlayers'
