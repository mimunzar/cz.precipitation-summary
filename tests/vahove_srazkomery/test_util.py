#!/usr/bin/env python3

import src.vahove_srazkomery.util as util


def test_sliding_window():
    assert list(util.sliding_window(2, range(0))) == []
    assert list(util.sliding_window(2, range(1))) == []
    assert list(util.sliding_window(2, range(2))) == [(0, 1)]
    assert list(util.sliding_window(2, range(3))) == [(0, 1), (1, 2)]

