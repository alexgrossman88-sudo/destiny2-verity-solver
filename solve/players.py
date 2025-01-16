from collections.abc import Mapping
from dataclasses import dataclass

from .shapes import Shape2D
from .states import PositionsType

type AliasMappingType = Mapping[PositionsType, str]


@dataclass(frozen=True, kw_only=True, slots=True)
class SoloPlayer:
    alias: str
    their_shape: Shape2D
    other_shape: Shape2D


@dataclass(frozen=True, kw_only=True, slots=True)
class MainRoomPlayers:
    dissector: str
    helper1: str
    helper2: str


__all__ = 'SoloPlayer', 'AliasMappingType', 'MainRoomPlayers'
