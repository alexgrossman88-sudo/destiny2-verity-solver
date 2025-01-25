from collections.abc import Callable, Sequence
from unittest import TestCase

from solve.combo import Combination
from solve.key_sets import *
from solve.move_analyzer import *
from solve.players import AllPlayers, Player
from solve.states import LEFT, MIDDLE, RIGHT, StateWithAllPositions
from . import move_count_dissection, move_count_rooms
from .combos import all_combinations


class TestMoveCount(TestCase):
    def setUp(self, /) -> None:
        self.all_players = AllPlayers(
            left=Player('A'),
            middle=Player('B'),
            right=Player('C'),
            dissector=Player('D'),
            helper1=Player('E'),
            helper2=Player('F'),
            )

    def _test_all[S, M](
            self,
            create_state: Callable[[Combination, KeySetType], StateWithAllPositions[S, M]],
            select_solution: Callable[
                [Sequence[StateWithAllPositions[S, M]]],
                tuple[StateWithAllPositions[S, M], Sequence[Step]],
            ],
            /,
            *,
            move_count_mixed: dict[str, int],
            move_count_double1: dict[str, int],
            move_count_double2: dict[str, int],
            step_count_mixed: dict[str, int],
            step_count_double1: dict[str, int],
            step_count_double2: dict[str, int],
            ) -> None:
        solve_args = (False, None), (True, LEFT), (True, MIDDLE), (True, RIGHT)
        params = zip(
            (KS_MIXED, KS_DOUBLE_1, KS_DOUBLE_2),
            ('KS_MIXED', 'KS_DOUBLE_1', 'KS_DOUBLE_2'),
            (move_count_mixed, move_count_double1, move_count_double2),
            (step_count_mixed, step_count_double1, step_count_double2),
            )
        for ks, ks_name, move_counts, step_counts in params:
            for code, combo in all_combinations.items():
                expected_move_count = move_counts[code]
                expected_step_count = step_counts[code]
                state = create_state(combo, ks)
                for with_triumph, last_position in solve_args:
                    with self.subTest(
                            ks=ks_name,
                            code=code,
                            with_triumph=with_triumph,
                            last_position=last_position,
                            ):
                        solutions = state.solve(with_triumph, last_position)
                        best, steps = select_solution(solutions)
                        self.assertEqual(expected_move_count, len(best.moves_made))
                        # Number of dissection steps can be less than expected.
                        # Usually, the number of steps are
                        # expected_move_count + expected_move_count // 3
                        # but one extra step is required
                        # when doing both challenge and triumph with specific last position.
                        # For example,0[00]-3[34]-4[43] is solved in 9 steps
                        # when middle is the last position,
                        # and is solved in 8 steps otherwise.
                        self.assertGreaterEqual(expected_step_count, len(steps))

    def test_rooms(self, /) -> None:
        self._test_all(
            Combination.to_room_state,
            lambda seq: best_solution(seq, self.all_players, describe_pass_moves),
            move_count_mixed=move_count_rooms.number_of_moves_mixed,
            move_count_double1=move_count_rooms.number_of_moves_double1,
            move_count_double2=move_count_rooms.number_of_moves_double2,
            step_count_mixed=move_count_rooms.number_of_steps_mixed,
            step_count_double1=move_count_rooms.number_of_steps_double1,
            step_count_double2=move_count_rooms.number_of_steps_double2,
            )

    def test_dissection(self, /) -> None:
        self._test_all(
            Combination.to_statue_state,
            lambda seq: best_solution(seq, self.all_players, describe_dissect_moves),
            move_count_mixed=move_count_dissection.number_of_moves_mixed,
            move_count_double1=move_count_dissection.number_of_moves_double1,
            move_count_double2=move_count_dissection.number_of_moves_double2,
            step_count_mixed=move_count_dissection.number_of_steps_mixed,
            step_count_double1=move_count_dissection.number_of_steps_double1,
            step_count_double2=move_count_dissection.number_of_steps_double2,
            )
