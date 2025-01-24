import operator
from collections.abc import Callable
from typing import Any
from unittest import TestCase

from solve.multiset import Multiset


# TODO add tests for MutableMultiset too
#  think about fixtures for cases with inline operators
class TestMultisetWithSet(TestCase):
    def setUp(self, /) -> None:
        self.set1 = frozenset({'a', 'c'})
        self.set2 = frozenset({'c', 'e'})
        self.multiset1 = Multiset(self.set1)
        self.multiset2 = Multiset(self.set2)

    def test_equality(self, /) -> None:
        self.assertEqual(self.set1, self.multiset1)
        self.assertEqual(self.multiset1, self.set1)
        self.assertEqual(self.set2, self.multiset2)
        self.assertEqual(self.multiset2, self.set2)

    def test_hash_equality(self, /) -> None:
        self.assertEqual(hash(self.set1), hash(self.multiset1))
        self.assertEqual(hash(self.set2), hash(self.multiset2))

    def test_inequality(self, /) -> None:
        self.assertNotEqual(self.multiset1, self.multiset2)
        self.assertNotEqual(self.set1, self.multiset2)
        self.assertNotEqual(self.multiset2, self.set1)
        self.assertNotEqual(self.set2, self.multiset1)
        self.assertNotEqual(self.multiset1, self.set2)

    def _test_op(
            self,
            op: Callable[[Any, Any], Any],
            expected_values: dict[str, Any],
            /,
            *,
            commutative: bool = False,
            ) -> None:
        v = dict(
            set1_op_set2=op(self.set1, self.set2),
            set1_op_mset1=op(self.set1, self.multiset1),
            set1_op_mset2=op(self.set1, self.multiset2),

            set2_op_set1=op(self.set2, self.set1),
            set2_op_mset1=op(self.set2, self.multiset1),
            set2_op_mset2=op(self.set2, self.multiset2),

            mset1_op_set1=op(self.multiset1, self.set1),
            mset1_op_set2=op(self.multiset1, self.set2),
            mset1_op_mset2=op(self.multiset1, self.multiset2),

            mset2_op_set1=op(self.multiset2, self.set1),
            mset2_op_set2=op(self.multiset2, self.set2),
            mset2_op_mset1=op(self.multiset2, self.multiset1),
            )

        self.assertEqual(v['set1_op_set2'], v['mset1_op_mset2'])
        self.assertEqual(v['set2_op_set1'], v['mset2_op_mset1'])

        for name, actual in v.items():
            self.assertEqual(expected_values[name], actual)

        if commutative:
            self.assertEqual(v['set1_op_mset1'], v['mset1_op_set1'])
            self.assertEqual(v['set1_op_mset2'], v['mset2_op_set1'])
            self.assertEqual(v['set2_op_mset1'], v['mset1_op_set2'])
            self.assertEqual(v['set2_op_mset2'], v['mset2_op_set2'])
            self.assertEqual(v['mset1_op_mset2'], v['mset2_op_mset1'])

        self.assertIsNot(self.multiset1, v['set1_op_mset1'])
        self.assertIsNot(self.multiset2, v['set1_op_mset2'])
        self.assertIsNot(self.multiset1, v['set2_op_mset1'])
        self.assertIsNot(self.multiset2, v['set2_op_mset2'])

        self.assertIsNot(self.multiset1, v['mset1_op_set1'])
        self.assertIsNot(self.multiset1, v['mset1_op_set2'])
        self.assertIsNot(self.multiset1, v['mset1_op_mset2'])
        self.assertIsNot(self.multiset2, v['mset1_op_mset2'])

        self.assertIsNot(self.multiset2, v['mset2_op_set1'])
        self.assertIsNot(self.multiset2, v['mset2_op_set2'])
        self.assertIsNot(self.multiset2, v['mset2_op_mset1'])
        self.assertIsNot(self.multiset1, v['mset2_op_mset1'])

    def test_lt(self, /) -> None:
        same1 = False
        same2 = False
        both = False
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.lt, v)

    def test_le(self, /) -> None:
        same1 = True
        same2 = True
        both = False
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.le, v)

    def test_gt(self, /) -> None:
        same1 = False
        same2 = False
        both = False
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.gt, v)

    def test_ge(self, /) -> None:
        same1 = True
        same2 = True
        both = False
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.ge, v)

    def test_union(self, /) -> None:
        same1 = {'a', 'c'}
        same2 = {'c', 'e'}
        both = {'a', 'c', 'e'}
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.or_, v, commutative=True)
        self._test_op(operator.ior, v, commutative=True)

    def test_intersection(self, /) -> None:
        same1 = {'a', 'c'}
        same2 = {'c', 'e'}
        both = {'c'}
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.and_, v, commutative=True)
        self._test_op(operator.iand, v, commutative=True)

    def test_symmetric_difference(self, /) -> None:
        same1 = set()
        same2 = set()
        both = {'a', 'e'}
        v = dict(
            set1_op_set2=both,
            set1_op_mset1=same1,
            set1_op_mset2=both,

            set2_op_set1=both,
            set2_op_mset1=both,
            set2_op_mset2=same2,

            mset1_op_set1=same1,
            mset1_op_set2=both,
            mset1_op_mset2=both,

            mset2_op_set1=both,
            mset2_op_set2=same2,
            mset2_op_mset1=both,
            )
        self._test_op(operator.xor, v, commutative=True)
        self._test_op(operator.ixor, v, commutative=True)

    def test_difference(self, /) -> None:
        one_two = {'a'}
        two_one = {'e'}
        same = set()
        v = dict(
            set1_op_set2=one_two,
            set1_op_mset1=same,
            set1_op_mset2=one_two,

            set2_op_set1=two_one,
            set2_op_mset1=two_one,
            set2_op_mset2=same,

            mset1_op_set1=same,
            mset1_op_set2=one_two,
            mset1_op_mset2=one_two,

            mset2_op_set1=two_one,
            mset2_op_set2=same,
            mset2_op_mset1=two_one,
            )
        self._test_op(operator.sub, v)
        self._test_op(operator.isub, v)

    def test_addition(self, /) -> None:
        same1 = Multiset({'a': 2, 'c': 2})
        same2 = Multiset({'c': 2, 'e': 2})
        both = Multiset({'a': 1, 'c': 2, 'e': 1})

        for op in (operator.add, operator.iadd):
            set1_op_mset1 = op(self.set1, self.multiset1)
            set1_op_mset2 = op(self.set1, self.multiset2)

            set2_op_mset1 = op(self.set2, self.multiset1)
            set2_op_mset2 = op(self.set2, self.multiset2)

            mset1_op_set1 = op(self.multiset1, self.set1)
            mset1_op_set2 = op(self.multiset1, self.set2)
            mset1_op_mset2 = op(self.multiset1, self.multiset2)

            mset2_op_set1 = op(self.multiset2, self.set1)
            mset2_op_set2 = op(self.multiset2, self.set2)
            mset2_op_mset1 = op(self.multiset2, self.multiset1)

            self.assertEqual(self.set1 | self.set2, both)

            self.assertEqual(same1, set1_op_mset1)
            self.assertEqual(same1, mset1_op_set1)
            self.assertEqual(same2, set2_op_mset2)
            self.assertEqual(same2, mset2_op_set2)
            self.assertEqual(both, set1_op_mset2)
            self.assertEqual(both, set2_op_mset1)
            self.assertEqual(both, mset1_op_set2)
            self.assertEqual(both, mset1_op_mset2)
            self.assertEqual(both, mset2_op_set1)
            self.assertEqual(both, mset2_op_mset1)

            self.assertIsNot(self.multiset1, set1_op_mset1)
            self.assertIsNot(self.multiset1, mset1_op_set1)
            self.assertIsNot(self.multiset2, set2_op_mset2)
            self.assertIsNot(self.multiset2, mset2_op_set2)
            self.assertIsNot(self.multiset2, set1_op_mset2)
            self.assertIsNot(self.multiset1, set2_op_mset1)
            self.assertIsNot(self.multiset1, mset1_op_set2)
            self.assertIsNot(self.multiset1, mset1_op_mset2)
            self.assertIsNot(self.multiset2, mset1_op_mset2)
            self.assertIsNot(self.multiset2, mset2_op_set1)
            self.assertIsNot(self.multiset1, mset2_op_mset1)
            self.assertIsNot(self.multiset2, mset2_op_mset1)
