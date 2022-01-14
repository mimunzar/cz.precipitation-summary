#!/usr/bin/env python3

import itertools as it

import src.precipitation_summary.data as data


def test_iter_rain_rows():
    fake_data = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
    )
    to_tuple = lambda it: tuple(map(tuple, it))
    assert to_tuple(data.iter_rain_rows(fake_data, (0, 0))) == fake_data
    assert to_tuple(data.iter_rain_rows(fake_data, (1, 2))) == ((6,), (9,))
    assert to_tuple(data.iter_rain_rows(fake_data, (3, 3))) == ()
    assert to_tuple(data.iter_rain_rows(fake_data, (4, 4))) == ()


class FakeCell:
    def __init__(self, column_letter, value):
        self.column_letter = column_letter
        self.value         = value


def test_parse_rain_data():
    fake_data = (
        (FakeCell('A', 1), FakeCell('B', 2)),
        (FakeCell('A', 3), FakeCell('B', None)),
    )
    assert dict(data.parse_rain_data(tuple()))   == {}
    assert dict(data.parse_rain_data(it.islice(fake_data, 0, 1))) == {
            'A': [1],
            'B': [2],
        }
    assert dict(data.parse_rain_data(it.islice(fake_data, 0, None))) == {
            'A': [1, 3],
            'B': [2, 0],
        }


def test_iter_rain_data():
    assert tuple(data.iter_rain_data({})) == tuple()
    assert tuple(data.iter_rain_data({'A': [1, 3]})) == (
            (0, 1), (1, 3),
        )
    assert tuple(data.iter_rain_data({'A': [1, 3], 'B': [2, 4]})) == (
            (0, 1), (1, 3), (2, 2), (3, 4),
        )

