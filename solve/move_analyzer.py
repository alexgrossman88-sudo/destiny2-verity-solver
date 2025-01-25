from collections import defaultdict, deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from itertools import batched
from typing import Any, Self

from .players import AllPlayers, Player
from .shapes import Shape2D
from .states import (
    DissectMove,
    KNIGHTS_PER_SPAWN,
    PassMove,
    PositionsType,
    SHAPE_TO_KNIGHT_POSITION,
    )


@dataclass(frozen=True, slots=True)
class Step:
    """
    A single step in the encounter solution.
    """
    description: str
    params: Mapping[str, Any]

    def __init__(self, description: str, /, **kwargs: Any) -> None:
        object.__setattr__(self, 'description', description)
        object.__setattr__(self, 'params', kwargs)

    def render(self, /) -> str:
        """
        Converts this step to a string.
        """
        return self.description.format_map(self.params)

    @classmethod
    def collect(
            cls,
            player: Player,
            shape: Shape2D,
            /,
            with_knight: bool = False,
            ) -> Self:
        if with_knight:
            return cls(
                'Player {player}: kill {position} knight and collect {shape}',
                player=player,
                shape=shape,
                position=SHAPE_TO_KNIGHT_POSITION[shape],
                )

        return cls(
            'Player {player}: collect {shape}',
            player=player,
            shape=shape,
            )

    @classmethod
    def pass_(cls, player: Player, shape: Shape2D, position: PositionsType, /) -> Self:
        return cls(
            'Player {player}: pass {shape} to {position}',
            player=player,
            shape=shape,
            position=position,
            )

    @classmethod
    def dissect(
            cls,
            player: Player,
            shape: Shape2D,
            destination: PositionsType,
            /,
            to_collect: bool = False,
            ) -> Self:
        if to_collect:
            return cls(
                'Player {player}: kill {position} knight, '
                'collect {shape} and dissect {destination}',
                player=player,
                shape=shape,
                position=SHAPE_TO_KNIGHT_POSITION[shape],
                destination=destination,
                )

        return cls(
            'Player {player}: dissect {destination}',
            player=player,
            destination=destination,
            )


def describe_pass_moves(
        moves_made: Sequence[PassMove],
        players: AllPlayers,
        /,
        ) -> Sequence[Step]:
    """
    Returns a sequence of verbosely described steps
    required to perform the given sequence of :class:`PassMove`.
    """
    departure2collect = defaultdict(deque)
    for m in moves_made:
        departure2collect[m.departure].appendleft(m.shape)

    steps = [
        Step.collect(players.solo_player(position), shapes.pop())
        for position, shapes in departure2collect.items()
        ]

    destination2collect = defaultdict(deque)
    for m in moves_made:
        steps.append(Step.pass_(players.solo_player(m.departure), m.shape, m.destination))

        shapes = departure2collect[m.departure]
        if shapes:
            shape = shapes.pop()
            if shape in m.departure_state:
                steps.append(Step.collect(players.solo_player(m.departure), shape))
            else:
                destination2collect[m.departure].appendleft(shape)

        shapes = destination2collect[m.destination]
        if shapes and shapes[-1] in m.destination_state:
            steps.append(Step.collect(players.solo_player(m.destination), shapes.pop()))

    return steps


@dataclass(slots=True)
class ShapeHolders:
    players: AllPlayers
    dissector_shape: Shape2D | None = None
    helper1_shape: Shape2D | None = None
    helper2_shape: Shape2D | None = None

    def collect_shape(self, shape: Shape2D, /) -> Player:
        """
        Determines the available player to collect the given shape.
        """
        if self.helper1_shape is None:
            self.helper1_shape = shape
            player = self.players.helper1
        elif self.helper2_shape is None:
            self.helper2_shape = shape
            player = self.players.helper2
        elif self.dissector_shape is None:
            self.dissector_shape = shape
            player = self.players.dissector
        else:
            raise RuntimeError(
                'all players in the main room already hold a shape, '
                f'cannot collect {shape}, {self}'
                )

        return player

    def dissect(self, shape: Shape2D, /) -> Player:
        """
        Determines the available player to dissect with the given shape.
        """
        if self.dissector_shape == shape:
            self.dissector_shape = None
            player = self.players.dissector
        elif self.helper1_shape == shape:
            self.helper1_shape = None
            player = self.players.helper1
        elif self.helper2_shape == shape:
            self.helper2_shape = None
            player = self.players.helper2
        else:
            raise RuntimeError(
                'no player in the main room holds shape, '
                f'cannot dissect with {shape}, {self}'
                )

        return player

    def __contains__(self, item: Shape2D, /) -> bool:
        return item in (self.helper1_shape, self.helper2_shape, self.dissector_shape)


def describe_dissect_moves(
        moves_made: Sequence[DissectMove],
        players: AllPlayers,
        /,
        ) -> Sequence[Step]:
    """
    Returns a sequence of verbosely described steps
    required to perform the given sequence of :class:`DissectMove`.
    """
    steps = []
    shape_holders = ShapeHolders(players)
    move_batches = batched(moves_made, KNIGHTS_PER_SPAWN)
    moves: list[DissectMove] = list(next(move_batches))
    while moves:
        shapes_to_collect = set(SHAPE_TO_KNIGHT_POSITION)
        pending_moves = moves.copy()
        moves = []

        for m in pending_moves:
            if m.shape in shape_holders:
                player = shape_holders.dissect(m.shape)
                steps.append(Step.dissect(player, m.shape, m.destination))
            elif m.shape in shapes_to_collect:
                shapes_to_collect.remove(m.shape)
                # Add one step if dissector is available, and two otherwise.
                # This forces solutions with such situations to be worse.
                if shape_holders.dissector_shape is None:
                    steps.append(Step.dissect(players.dissector, m.shape, m.destination, True))
                else:
                    player = shape_holders.collect_shape(m.shape)
                    steps.append(Step.collect(player, m.shape, with_knight=True))
                    player = shape_holders.dissect(m.shape)
                    steps.append(Step.dissect(player, m.shape, m.destination))
            else:
                moves.append(m)
                while shapes_to_collect:
                    shape = shapes_to_collect.pop()
                    player = shape_holders.collect_shape(shape)
                    steps.append(Step.collect(player, shape, with_knight=True))

        next_moves = next(move_batches, None)
        if next_moves:
            moves.extend(next_moves)

        if not shapes_to_collect:
            steps.append(Step('All players: kill champions'))

    return steps


def best_solution[SM, M](
        states: Sequence[SM],
        all_players: AllPlayers,
        describe_func: Callable[[Sequence[M], AllPlayers], Sequence[Step]],
        /,
        ) -> tuple[SM, Sequence[Step]]:
    """
    Takes a sequence of solved states
    and a function which describes sequences of moves given players,
    decides the best solution and returns it with its steps.

    The best solution is the solution with the minimum number of steps.
    """
    it = iter(states)
    best = next(it)
    best_steps = describe_func(best.moves_made, all_players)
    for state in it:
        steps = describe_func(state.moves_made, all_players)
        if len(steps) < len(best_steps):
            best = state
            best_steps = steps

    return best, best_steps


__all__ = 'Step', 'describe_pass_moves', 'describe_dissect_moves', 'best_solution'
