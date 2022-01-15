#!/usr/bin/env python3

import itertools as it

import src.precipitation_summary.data as data


class FakeCell:
    def __init__(self, column_letter, value):
        self.column_letter = column_letter
        self.value         = value


def test_parse_rain_data():
    fake_data = (
        (FakeCell('A', 1), FakeCell('B', 2)),
        (FakeCell('A', 3), FakeCell('B', None)),
    )
    assert dict(data.parse_data(tuple()))   == {}
    assert dict(data.parse_data(it.islice(fake_data, 0, 1))) == {
            'A': [(1, False)], 'B': [(2, False)]}
    assert dict(data.parse_data(it.islice(fake_data, 0, None))) == {
            'A': [(1, False), (3, False)], 'B': [(2, False), (0, True)]}


def test_iter_rain_data():
    assert tuple(data.iter_parsed({})) == tuple()
    fake_data = {'A': [(1, False), (3, False)]}
    assert tuple(data.iter_parsed(fake_data)) == ((0, 1, False), (1, 3, False),)
    fake_data = {'A': [(1, False), (3, False)], 'B': [(2, False), (4, True)]}
    assert tuple(data.iter_parsed(fake_data)) == (
            (0, 1, False), (1, 3, False), (2, 2, False), (3, 4, True),)

