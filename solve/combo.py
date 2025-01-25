from dataclasses import dataclass

from .key_sets import *
from .shapes import Shape2D
from .states import StateOfAllRooms, StateOfAllStatues, init_rooms, init_statues


@dataclass(frozen=True, kw_only=True, slots=True)
class Node:
    shade: Shape2D
    other: Shape2D

    @property
    def code(self, /) -> str:
        """
        Numeric code for this node.
        """
        return f'{self.shade.code}[{self.shade.code}{self.other.code}]'


@dataclass(frozen=True, kw_only=True, slots=True)
class Combination:
    left: Node
    middle: Node
    right: Node

    @property
    def code(self, /) -> str:
        """
        Numeric code for this combination.
        """
        return f'{self.left.code}-{self.middle.code}-{self.right.code}'

    def to_room_state(self, key_set: KeySetType, /) -> StateOfAllRooms:
        return init_rooms(
            left_shade=self.left.shade,
            left_other_shape=self.left.other,
            middle_shade=self.middle.shade,
            middle_other_shape=self.middle.other,
            right_shade=self.right.shade,
            right_other_shape=self.right.other,
            key_set=key_set,
            )

    def to_statue_state(self, key_set: KeySetType, /) -> StateOfAllStatues:
        return init_statues(
            left_shade=self.left.shade,
            left_3d_shape=self.left.shade + self.left.other,
            middle_shade=self.middle.shade,
            middle_3d_shape=self.middle.shade + self.middle.other,
            right_shade=self.right.shade,
            right_3d_shape=self.right.shade + self.right.other,
            key_set=key_set,
            )


code_to_best_ks = {
    '0[03]-3[34]-4[40]': KS_DOUBLE_2,
    '0[04]-3[30]-4[43]': KS_DOUBLE_1,
    '0[03]-4[40]-3[34]': KS_DOUBLE_2,
    '0[04]-4[43]-3[30]': KS_DOUBLE_1,
    '3[30]-0[04]-4[43]': KS_DOUBLE_1,
    '3[34]-0[03]-4[40]': KS_DOUBLE_2,
    '3[30]-4[43]-0[04]': KS_DOUBLE_1,
    '3[34]-4[40]-0[03]': KS_DOUBLE_2,
    '4[40]-0[03]-3[34]': KS_DOUBLE_2,
    '4[43]-0[04]-3[30]': KS_DOUBLE_1,
    '4[40]-3[34]-0[03]': KS_DOUBLE_2,
    '4[43]-3[30]-0[04]': KS_DOUBLE_1,
    }


def get_best_double_key(*, rooms: Combination | None, statues: Combination | None) -> KeySetType:
    """
    Determines the best double key set for provided combinations.

    At first evaluates the best key set for room combination.
    If there is no best key or the combination is not provided,
    then it uses statue combination for evaluation.
    If either evaluation is indifferent, returns ``KS_DOUBLE_1``.
    """
    if rooms is not None:
        best_ks = code_to_best_ks.get(rooms.code)
        if best_ks is not None:
            return best_ks

    if statues is not None:
        best_ks = code_to_best_ks.get(statues.code)
        if best_ks is not None:
            return best_ks

    return KS_DOUBLE_1


__all__ = 'Node', 'Combination', 'get_best_double_key'
