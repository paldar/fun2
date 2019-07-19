from typing import Iterable, List, Any, Callable, TypeVar, Iterator, Union
from functools import reduce, partial, singledispatch
from itertools import chain, compress, starmap
from operator import itemgetter, add, neg, attrgetter

T = TypeVar('T')


def noop(obj: T) -> T:
    return obj


def car(iterable: Iterable[T]):
    return next(iterable.__iter__())


def cdr(iterable: Iterable[T]):
    advanced_iter = iterable.__iter__()
    next(advanced_iter)
    return advanced_iter


class Fun:
    def __init__(self, iterable: Iterable[T]):
        self._data = list(iterable)
        self.operations = list()

    def map(self, ufunc: Callable[[T], Any]):
        self.operations.append(partial(map, ufunc))
        return self

    def reduce(self, binary_op: Callable[[T, T], Any]):
        self.operations.append(partial(reduce, binary_op))
        return self

    def filter(self, bool_op: Callable[[T], bool]):
        self.operations.extend([partial(filter, bool_op), list])
        return self

    def sum(self):
        self.operations.append(sum)
        return self

    def flatten(self):
        # stream must only contain items of the same type
        self.operations.append(partial(reduce, add))
        return self

    def sorted(self, key: noop, reverse: bool = False):
        # def _sorted_wrapper(key, reverse, data):
        #     return sorted(data, key=key, reverse=reverse)

        self.operations.append(partial(sorted, key=key, reverse=reverse))
        return self

    def reversed(self):
        self.operations.append(reversed)
        return self

    def min(self):
        self.operations.append(min)
        return self

    def max(self):
        self.operations.append(max)
        return self

    def negate(self):
        self.operations.append(partial(map, neg))
        return self

    def getitem(self, *args, **kwargs):
        self.operations.append(itemgetter(*args, **kwargs))
        return self

    def getattr(self, *args, **kwargs):
        self.operations.append(attrgetter(*args, **kwargs))
        return self

    def unique(self, by=noop):
        # TODO: allow generic uniqueness
        self.operations.extend([set, list])
        return self

    def mask(self, mask: Iterable[bool]):
        self.operations.extend(partial(compress, selectors=map(bool, mask)))
        return self

    def map_apply(self, ufunc):
        self.operations.extend(partial(starmap, ufunc))
        return self

    def collect(self):
        for func in self.operations:
            self._data = func(self._data)
        try:
            return list(self._data)
        except TypeError:
            return self._data
