#!/usr/bin/env python3

import collections as cl
import itertools   as it


def sliding_window(n, iterable):
    iterable = iter(iterable)
    window   = cl.deque(it.islice(iterable, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in iterable:
        window.append(x)
        yield tuple(window)

