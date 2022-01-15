#!/usr/bin/env python3

import collections as cl
import itertools   as it
import operator    as op


minutes = lambda n: n//10
hours   = lambda n: n*minutes(60)


def sliding_window(n, iterable):
    iterable = iter(iterable)
    window   = cl.deque(it.islice(iterable, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in iterable:
        window.append(x)
        yield tuple(window)


def dedupe(iterable):
    return map(next, map(op.itemgetter(1), it.groupby(iterable)))


def print_progress(bar_width, total, curr):
    ratio = min(curr, total)/total
    prog  = ('#'*round(ratio*bar_width)).ljust(bar_width)
    return f'[{prog}] {ratio:4.0%}'


def drop(n, iterable):
    return it.islice(iterable, n, None)


def value_chain(iterable):
    for i in iterable:
        try:
            yield from i
        except TypeError:
            yield i

