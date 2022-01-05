#!/usr/bin/env python3

import src.precipitation_summary.util as util


def test_sliding_window():
    assert list(util.sliding_window(2, range(0))) == []
    assert list(util.sliding_window(2, range(1))) == []
    assert list(util.sliding_window(2, range(2))) == [(0, 1)]
    assert list(util.sliding_window(2, range(3))) == [(0, 1), (1, 2)]


def test_dedupe():
    assert list(util.dedupe([])) == []
    assert list(util.dedupe([1, 1])) == [1]
    assert list(util.dedupe([1, 1, 2])) == [1, 2]
    assert list(util.dedupe([1, 1, 2, 1])) == [1, 2, 1]


def test_make_print_progress():
    assert util.print_progress(1, 1, 0) == '[ ]   0%'
    assert util.print_progress(1, 1, 1) == '[#] 100%'
    assert util.print_progress(1, 1, 2) == '[#] 100%'

    assert util.print_progress(5, 1, 0)    == '[     ]   0%'
    assert util.print_progress(5, 1, 0.33) == '[##   ]  33%'
    assert util.print_progress(5, 1, 1)    == '[#####] 100%'

    assert util.print_progress(10, 5, 0) == '[          ]   0%'
    assert util.print_progress(10, 5, 1) == '[##        ]  20%'
    assert util.print_progress(10, 5, 5) == '[##########] 100%'

