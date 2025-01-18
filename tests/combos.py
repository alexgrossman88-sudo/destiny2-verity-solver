from solve.combo import Combination, Node
from solve.shapes import circle, square, triangle

_all_combinations_n = 3 * 1 * 3 * 2 * 1 * 2 * 1 * 1 * 1
_all_combinations = [
    Combination(
        left=Node(shade=circle, other=circle),
        middle=Node(shade=triangle, other=triangle),
        right=Node(shade=square, other=square),
        ),
    Combination(
        left=Node(shade=circle, other=circle),
        middle=Node(shade=triangle, other=square),
        right=Node(shade=square, other=triangle),
        ),
    Combination(
        left=Node(shade=circle, other=triangle),
        middle=Node(shade=triangle, other=circle),
        right=Node(shade=square, other=square),
        ),
    Combination(
        left=Node(shade=circle, other=triangle),
        middle=Node(shade=triangle, other=square),
        right=Node(shade=square, other=circle),
        ),
    Combination(
        left=Node(shade=circle, other=square),
        middle=Node(shade=triangle, other=circle),
        right=Node(shade=square, other=triangle),
        ),
    Combination(
        left=Node(shade=circle, other=square),
        middle=Node(shade=triangle, other=triangle),
        right=Node(shade=square, other=circle),
        ),
    Combination(
        left=Node(shade=circle, other=circle),
        middle=Node(shade=square, other=triangle),
        right=Node(shade=triangle, other=square),
        ),
    Combination(
        left=Node(shade=circle, other=circle),
        middle=Node(shade=square, other=square),
        right=Node(shade=triangle, other=triangle),
        ),
    Combination(
        left=Node(shade=circle, other=triangle),
        middle=Node(shade=square, other=circle),
        right=Node(shade=triangle, other=square),
        ),
    Combination(
        left=Node(shade=circle, other=triangle),
        middle=Node(shade=square, other=square),
        right=Node(shade=triangle, other=circle),
        ),
    Combination(
        left=Node(shade=circle, other=square),
        middle=Node(shade=square, other=circle),
        right=Node(shade=triangle, other=triangle),
        ),
    Combination(
        left=Node(shade=circle, other=square),
        middle=Node(shade=square, other=triangle),
        right=Node(shade=triangle, other=circle),
        ),
    Combination(
        left=Node(shade=triangle, other=circle),
        middle=Node(shade=circle, other=triangle),
        right=Node(shade=square, other=square),
        ),
    Combination(
        left=Node(shade=triangle, other=circle),
        middle=Node(shade=circle, other=square),
        right=Node(shade=square, other=triangle),
        ),
    Combination(
        left=Node(shade=triangle, other=triangle),
        middle=Node(shade=circle, other=circle),
        right=Node(shade=square, other=square),
        ),
    Combination(
        left=Node(shade=triangle, other=triangle),
        middle=Node(shade=circle, other=square),
        right=Node(shade=square, other=circle),
        ),
    Combination(
        left=Node(shade=triangle, other=square),
        middle=Node(shade=circle, other=circle),
        right=Node(shade=square, other=triangle),
        ),
    Combination(
        left=Node(shade=triangle, other=square),
        middle=Node(shade=circle, other=triangle),
        right=Node(shade=square, other=circle),
        ),
    Combination(
        left=Node(shade=triangle, other=circle),
        middle=Node(shade=square, other=triangle),
        right=Node(shade=circle, other=square),
        ),
    Combination(
        left=Node(shade=triangle, other=circle),
        middle=Node(shade=square, other=square),
        right=Node(shade=circle, other=triangle),
        ),
    Combination(
        left=Node(shade=triangle, other=triangle),
        middle=Node(shade=square, other=circle),
        right=Node(shade=circle, other=square),
        ),
    Combination(
        left=Node(shade=triangle, other=triangle),
        middle=Node(shade=square, other=square),
        right=Node(shade=circle, other=circle),
        ),
    Combination(
        left=Node(shade=triangle, other=square),
        middle=Node(shade=square, other=circle),
        right=Node(shade=circle, other=triangle),
        ),
    Combination(
        left=Node(shade=triangle, other=square),
        middle=Node(shade=square, other=triangle),
        right=Node(shade=circle, other=circle),
        ),
    Combination(
        left=Node(shade=square, other=circle),
        middle=Node(shade=circle, other=triangle),
        right=Node(shade=triangle, other=square),
        ),
    Combination(
        left=Node(shade=square, other=circle),
        middle=Node(shade=circle, other=square),
        right=Node(shade=triangle, other=triangle),
        ),
    Combination(
        left=Node(shade=square, other=triangle),
        middle=Node(shade=circle, other=circle),
        right=Node(shade=triangle, other=square),
        ),
    Combination(
        left=Node(shade=square, other=triangle),
        middle=Node(shade=circle, other=square),
        right=Node(shade=triangle, other=circle),
        ),
    Combination(
        left=Node(shade=square, other=square),
        middle=Node(shade=circle, other=circle),
        right=Node(shade=triangle, other=triangle),
        ),
    Combination(
        left=Node(shade=square, other=square),
        middle=Node(shade=circle, other=triangle),
        right=Node(shade=triangle, other=circle),
        ),
    Combination(
        left=Node(shade=square, other=circle),
        middle=Node(shade=triangle, other=triangle),
        right=Node(shade=circle, other=square),
        ),
    Combination(
        left=Node(shade=square, other=circle),
        middle=Node(shade=triangle, other=square),
        right=Node(shade=circle, other=triangle),
        ),
    Combination(
        left=Node(shade=square, other=triangle),
        middle=Node(shade=triangle, other=circle),
        right=Node(shade=circle, other=square),
        ),
    Combination(
        left=Node(shade=square, other=triangle),
        middle=Node(shade=triangle, other=square),
        right=Node(shade=circle, other=circle),
        ),
    Combination(
        left=Node(shade=square, other=square),
        middle=Node(shade=triangle, other=circle),
        right=Node(shade=circle, other=triangle),
        ),
    Combination(
        left=Node(shade=square, other=square),
        middle=Node(shade=triangle, other=triangle),
        right=Node(shade=circle, other=circle),
        ),
    ]

assert len(_all_combinations) == _all_combinations_n, \
    f'number of all combination must be {_all_combinations_n}'
all_combinations = {c.code: c for c in _all_combinations}
del _all_combinations, _all_combinations_n

__all__ = 'all_combinations',
