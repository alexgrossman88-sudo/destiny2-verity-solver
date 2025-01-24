from collections import defaultdict, deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from itertools import batched

from .players import AliasMappingType, MainRoomPlayers
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


def describe_pass_moves(
        moves_made: Sequence[PassMove],
        aliases: AliasMappingType,
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
        Step(f'Player {aliases[position]}: collect {shapes.pop()}')
        for position, shapes in departure2collect.items()
        ]

    destination2collect = defaultdict(deque)
    for m in moves_made:
        steps.append(
            Step(
                f'Player {aliases[m.departure]}: '
                f'pass {m.shape} to {m.destination}'
                )
            )

        shapes = departure2collect[m.departure]
        if shapes:
            shape = shapes.pop()
            if shape in m.departure_state:
                steps.append(Step(f'Player {aliases[m.departure]}: collect {shape}'))
            else:
                destination2collect[m.departure].appendleft(shape)

        shapes = destination2collect[m.destination]
        if shapes and shapes[-1] in m.destination_state.shapes_available:
            steps.append(
                Step(f'Player {aliases[m.destination]}: collect {shapes.pop()}')
                )

    return steps


@dataclass(slots=True)
class ShapeHolders:
    aliases: MainRoomPlayers
    helper1_shape: Shape2D | None = None
    helper2_shape: Shape2D | None = None

    def collect_shape(self, shape: Shape2D, /) -> Step:
        """
        Orders any available player to collect the given shape.
        """
        if self.helper1_shape is None:
            self.helper1_shape = shape
            name = self.aliases.helper1
        elif self.helper2_shape is None:
            self.helper2_shape = shape
            name = self.aliases.helper2
        else:
            raise RuntimeError(
                'all helpers in the main room already hold a shape, '
                f'cannot collect {shape}, {self}'
                )

        return Step(
            f'Player {name}: '
            f'kill {SHAPE_TO_KNIGHT_POSITION[shape]} knight '
            f'and collect {shape}'
            )

    def dissect(self, shape: Shape2D, position: PositionsType, /) -> Step:
        """
        Orders any available player to dissect the given statue with the given shape.
        """
        if self.helper1_shape == shape:
            self.helper1_shape = None
            name = self.aliases.helper1
        elif self.helper2_shape == shape:
            self.helper2_shape = None
            name = self.aliases.helper2
        else:
            raise RuntimeError(
                'no helper in the main room holds shape, '
                f'cannot dissect {position} with {shape}, {self}'
                )

        return Step(f'Player {name}: dissect {position}')

    def __contains__(self, item: Shape2D, /) -> bool:
        return item == self.helper1_shape or item == self.helper2_shape


def describe_dissect_moves(
        moves_made: Sequence[DissectMove],
        aliases: MainRoomPlayers,
        /,
        ) -> Sequence[Step]:
    """
    Returns a sequence of verbosely described steps
    required to perform the given sequence of :class:`DissectMove`.
    """
    steps = []
    shape_holders = ShapeHolders(aliases)
    move_batches = batched(moves_made, KNIGHTS_PER_SPAWN)
    moves: list[DissectMove] = list(next(move_batches))
    while moves:
        shapes_to_collect = set(SHAPE_TO_KNIGHT_POSITION)
        pending_moves = moves.copy()
        moves = []

        for m in pending_moves:
            if m.shape in shape_holders:
                steps.append(shape_holders.dissect(m.shape, m.destination))
            elif m.shape in shapes_to_collect:
                shapes_to_collect.remove(m.shape)
                steps.append(
                    Step(
                        f'Player {aliases.dissector}: '
                        f'kill {SHAPE_TO_KNIGHT_POSITION[m.shape]} knight, '
                        f'collect {m.shape} and dissect {m.destination}'
                        )
                    )
            else:
                moves.append(m)
                while shapes_to_collect:
                    steps.append(shape_holders.collect_shape(shapes_to_collect.pop()))

        next_moves = next(move_batches, None)
        if next_moves:
            moves.extend(next_moves)

        if not shapes_to_collect:
            steps.append(Step('All players: kill champions'))

    return steps


def best_solution[SM, M, A](
        states: Sequence[SM],
        aliases: A,
        describe_func: Callable[[Sequence[M], A], Sequence[Step]],
        /,
        ) -> tuple[SM, Sequence[Step]]:
    """
    Takes a sequence of solved states
    and a function which describes sequences of moves given aliases,
    decides the best solution and returns it with its steps.

    The best solution sis the solution with the minimum number of steps.
    """
    it = iter(states)
    best = next(it)
    best_steps = describe_func(best.moves_made, aliases)
    for state in it:
        steps = describe_func(state.moves_made, aliases)
        if len(steps) < len(best_steps):
            best = state
            best_steps = steps

    return best, best_steps


__all__ = 'Step', 'describe_pass_moves', 'describe_dissect_moves', 'best_solution'
