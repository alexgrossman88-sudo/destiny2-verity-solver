import tomllib
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any

from .combo import Combination, Node
from .players import *
from .shapes import *
from .states.base import ALL_POSITIONS, LEFT, MIDDLE, PositionsType, RIGHT, is_position


class KeySetName(Enum):
    MIXED = 'mixed'
    DOUBLE = 'double'


@dataclass(frozen=True, kw_only=True, slots=True)
class Config:
    key_set_name: KeySetName
    shades: tuple[Shape2D, Shape2D, Shape2D]
    solo_players: tuple[SoloPlayer, SoloPlayer, SoloPlayer]
    shapes_3d: tuple[Shape3D, Shape3D, Shape3D]
    main_room_players: MainRoomPlayers
    is_doing_triumph: bool
    last_position: PositionsType | None

    def encounter_data(self, /) -> tuple[Combination, Combination, AliasMappingType]:
        """
        Extracts room combination, statue combination and alias mapping from this config.
        """
        shades = self.shades
        shade2person = {
            i: p
            for i in shades
            for p in self.solo_players
            if p.their_shape == i
            }
        aliases = dict(zip(ALL_POSITIONS, (shade2person[i].alias for i in shades)))
        other = tuple(shade2person[i].other_shape for i in shades)

        rooms = Combination(
            left=Node(shade=shades[0], other=other[0]),
            middle=Node(shade=shades[1], other=other[1]),
            right=Node(shade=shades[2], other=other[2]),
            )

        shapes_3d = self.shapes_3d
        statues = Combination(
            left=Node(shade=shades[0], other=shapes_3d[0] - shades[0]),
            middle=Node(shade=shades[1], other=shapes_3d[1] - shades[1]),
            right=Node(shade=shades[2], other=shapes_3d[2] - shades[2]),
            )

        return rooms, statues, aliases


_number_to_2d_shape = {
    circle.code:   circle,
    triangle.code: triangle,
    square.code:   square,
    }
_number_to_3d_shape = {
    20: sphere,
    23: pyramid,
    33: pyramid,
    24: cube,
    44: cube,

    30: cone,
    40: cylinder,
    34: prism,
    43: prism,
    }

_solo_player_fields = {field.name for field in fields(SoloPlayer)}
_main_room_fields = {'3d_shapes', 'dissector_alias', 'helper1_alias', 'helper2_alias'}


def is_non_empty_string(s: Any, /) -> bool:
    """
    Returns ``True``, if the given value is a string
    which is not empty or consists of only white spaces.
    Returns ``False`` otherwise.
    """
    return s and isinstance(s, str) and not s.isspace()


def read_config(filepath: str, /) -> Config:
    """
    Reads configuration file from provided filepath
    and returns an instance of :class:`Config`.
    """
    with open(filepath, 'rb') as f:
        data = tomllib.load(f)

    key_set_name = data.get('key_set', KeySetName.MIXED.value)
    assert key_set_name in KeySetName, \
        f'key_set must be either {KeySetName.MIXED.value!r} or {KeySetName.DOUBLE.value!r}'

    is_doing_triumph = data.get('is_doing_triumph', False)
    assert isinstance(is_doing_triumph, bool), 'is_doing_triumph must be a boolean'

    last_position = data.get('last_position', '')
    if last_position == '':
        last_position = None

    assert last_position is None or is_position(last_position), \
        f'last_position must be \'\', {LEFT!r}, {MIDDLE!r} or {RIGHT!r}'

    shades = data.get('shades')
    assert isinstance(shades, list) and set(shades) == _number_to_2d_shape.keys(), \
        f'shades must be a permutation of [0, 3, 4]'

    shades_gen = (_number_to_2d_shape[i] for i in shades)

    players = []
    for i, p in enumerate(map(data.get, ('player1', 'player2', 'player3')), 1):
        assert isinstance(p, dict) and p.keys() == _solo_player_fields, \
            f'player{i} must be a mapping ' \
            f'and have values for fields {', '.join(_solo_player_fields)}'

        alias = p['alias']
        assert is_non_empty_string(alias), f'alias of player{i} must be a non-empty string'

        their_shape = p['their_shape']
        other_shape = p['other_shape']
        assert their_shape in _number_to_2d_shape and other_shape in _number_to_2d_shape, \
            f'their_shape and other_shape of player{i} must be 0, 3 or 4'

        players.append(
            SoloPlayer(
                alias=alias.strip(),
                their_shape=_number_to_2d_shape[their_shape],
                other_shape=_number_to_2d_shape[other_shape],
                )
            )

    main_room = data.get('main_room')
    assert isinstance(main_room, dict) and main_room.keys() == _main_room_fields, \
        f'main_room must be a mapping and have values for fields {', '.join(_main_room_fields)}'

    shapes_3d = main_room['3d_shapes']
    assert (
            isinstance(shapes_3d, list)
            and len(shapes_3d) == 3
            and set(shapes_3d) <= _number_to_3d_shape.keys()
    ), f'3d_shapes must be a list of three numbers representing 3D shapes'

    shapes_3d_gen = (_number_to_3d_shape[i] for i in shapes_3d)

    dissector = main_room['dissector_alias']
    helper1 = main_room['helper1_alias']
    helper2 = main_room['helper2_alias']
    assert (
            is_non_empty_string(dissector)
            and is_non_empty_string(helper1)
            and is_non_empty_string(helper2)
    ), f'aliases of players in the main room must be non-empty strings'

    main_room_players = MainRoomPlayers(
        dissector=dissector.strip(),
        helper1=helper1.strip(),
        helper2=helper2.strip(),
        )

    return Config(
        key_set_name=KeySetName(key_set_name),
        shades=(next(shades_gen), next(shades_gen), next(shades_gen)),
        solo_players=(players[0], players[1], players[2]),
        shapes_3d=(next(shapes_3d_gen), next(shapes_3d_gen), next(shapes_3d_gen)),
        main_room_players=main_room_players,
        is_doing_triumph=is_doing_triumph,
        last_position=last_position,
        )


__all__ = 'KeySetName', 'Config', 'read_config'
