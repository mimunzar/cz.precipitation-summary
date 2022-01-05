#!/usr/bin/env python3

import src.precipitation_summary.make_summary as make_summary

import itertools as it


def test_is_heavy_rain():
    assert make_summary.is_heavy_rain(()) == False
    assert make_summary.is_heavy_rain(it.islice(it.repeat((0, 3)), 4)) == False
    assert make_summary.is_heavy_rain(it.islice(it.repeat((0, 3)), 5)) == True
    #^ The amount is higher than 12.5 mm in total
    assert make_summary.is_heavy_rain(it.islice(it.repeat((0, 5)), 1)) == False
    assert make_summary.is_heavy_rain(it.islice(it.repeat((0, 5)), 2)) == True
    #^ The amount per 20 minutes is than 8.3 mm

