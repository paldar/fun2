import unittest
from operator import add, itemgetter
from f2 import Fun, car


def _add1(val: int):
    return val + 1


class TestF2Chaining(unittest.TestCase):

    def test_map(self):
        range_size = 320000

        result = Fun(range(range_size)).map(_add1).collect()
        self.assertListEqual(list(range(1, range_size + 1)), result)

    def test_map_apply(self):
        range_size = 320000

        leftval = Fun(range(range_size)).map(_add1).collect()
        expected = list(range(1, range_size + 1))

        self.assertListEqual(leftval, expected)

    def test_reduce(self):
        range_size = 320000
        result = Fun(range(range_size)).map(_add1).reduce(add).collect()
        self.assertEqual(sum(range(range_size)) + range_size, result)

    def test_filter(self):
        range_size = 320000
        result = Fun(range(range_size)).filter(lambda x: x < 5).collect()
        self.assertListEqual(result, list(range(5)))

    def test_sorted(self):
        data = [{
            'name': 'Johanna',
            'title': 'Director',
        }, {
            'name': 'Susanna',
            'title': 'Architect',
        }, {
            'name': 'Edvard',
            'title': 'Janitorial Engineer',
        }, {
            'name': 'Pekka',
            'title': 'Blackboard Wiping Specialist',
        }]
        result = (Fun(data)
                  .sorted(key=itemgetter('name'), reverse=True)
                  .map(itemgetter('name'))
                  .collect())
        self.assertListEqual(result, ['Susanna', 'Pekka', 'Johanna', 'Edvard'])

    def test_flatmap(self):
        sep = 1299
        end = 3700
        delta = 1
        data = [list(range(sep)), list(range(sep, end))]
        result = Fun(data).flatmap(lambda x: x + delta).collect()
        self.assertListEqual(result, list(range(delta, end + delta)))
