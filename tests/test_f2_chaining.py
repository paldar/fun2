import unittest
from operator import add
from f2 import Fun


def _add1(val: int):
    return val + 1


class TestFunfunChaining(unittest.TestCase):

    def test_map(self):
        range_size = 320000

        result = Fun(range(range_size)).map(_add1).collect()
        self.assertListEqual(list(range(1, range_size + 1)), result)

    def test_map_apply(self):
        range_size = 320000

        result = Fun(range(range_size)).map(_add1).reduce(add).collect()
        self.assertEqual(sum(range(range_size)) + range_size, result)
