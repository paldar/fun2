from functools import reduce, partial
from itertools import compress, starmap
from operator import itemgetter, attrgetter, le, ge
from typing import Iterable, List, Any, Callable, TypeVar

T = TypeVar('T')
ReturnType = TypeVar('ReturnType')


def noop(obj: T) -> T:
    return obj


def car(iterable: Iterable[T]):
    return next(iterable.__iter__())


def cdr(iterable: Iterable[T]):
    advanced_iter = iterable.__iter__()
    next(advanced_iter)
    return advanced_iter


# TODO: benchmark this
def _generic_flatten_v1(obj: Iterable[Iterable[T]]) -> List[T]:
    return [val for sublist in obj for val in sublist]


class Fun:
    def __init__(self, iterable: Iterable[T]):
        self._data = list(iterable)
        self.operations: List[Callable] = list()

    def map(self, ufunc: Callable[[T], ReturnType]):
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
        self.operations.append(_generic_flatten_v1)
        return self

    def sorted(self, key: Callable = noop, reverse: bool = False):
        self.operations.append(partial(sorted, key=key, reverse=reverse))
        return self

    def reversed(self):
        self.operations.append(reversed)
        return self

    def getitem(self, *args, **kwargs):
        self.operations.append(itemgetter(*args, **kwargs))
        return self

    def getattr(self, *args, **kwargs):
        self.operations.append(attrgetter(*args, **kwargs))
        return self

    def mask(self, mask: Iterable[bool]):
        self.operations.append(partial(compress, selectors=map(bool, mask)))
        return self

    def map_apply(self, ufunc):
        self.operations.append(partial(starmap, ufunc))
        return self

    def flatmap(self, ufunc):
        self.operations.extend([_generic_flatten_v1, partial(map, ufunc)])
        return self

    def collect(self):
        for func in self.operations:
            self._data = func(self._data)
        try:
            return list(self._data)
        except TypeError:
            return self._data
