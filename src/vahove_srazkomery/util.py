#!/usr/bin/env python3

import collections as cl
import itertools   as it
import operator    as op


def sliding_window(n, iterable):
    iterable = iter(iterable)
    window   = cl.deque(it.islice(iterable, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in iterable:
        window.append(x)
        yield tuple(window)


def dedupe(iterable):
    return map(op.itemgetter(0), it.groupby(iterable))

