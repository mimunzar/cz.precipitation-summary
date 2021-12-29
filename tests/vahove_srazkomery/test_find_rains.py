#!/usr/bin/env python3


import src.vahove_srazkomery.find_rains as find_rains


def test_iter_rain_events():
    assert list(find_rains.iter_rain_events(0, 1, [])) == []
    rain_data = [(0, 1)]
    assert list(find_rains.iter_rain_events(1, 1, rain_data)) == [
            ((0, 1),)]
    rain_data = [(0, 0), (1, 1)]
    assert list(find_rains.iter_rain_events(2, 1, rain_data)) == [
            ((0, 0), (1, 1))]
    rain_data = [(0, 0), (1, 1), (2, 1)]
    assert list(find_rains.iter_rain_events(2, 1, rain_data)) == [
            ((0, 0), (1, 1)),
            ((1, 1), (2, 1))]


def test_iter_consecutive_events():
    assert list(find_rains.iter_consecutive_events([])) == []
    events = [((0, 0),)]
    assert list(find_rains.iter_consecutive_events(events)) == [
            [((0, 0),)]]
    events = [((0, 0),), ((1, 0),)]
    assert list(find_rains.iter_consecutive_events(events)) == [
            [((0, 0),), ((1, 0),)]]
    events = [((0, 0),), ((1, 0),), ((3, 0),), ((5, 0),), ((6, 0),)]
    assert list(find_rains.iter_consecutive_events(events)) == [
            [((0, 0),), ((1, 0),)],
            [((3, 0),)],
            [((5, 0),), ((6, 0),)]]


def test_merge_consecutive_events():
    assert list(find_rains.merge_consecutive_events([])) == []
    events = [((0, 0), (1, 0))]
    assert list(find_rains.merge_consecutive_events(events)) == [
            (0, 0), (1, 0)]
    events = [((0, 0), (1, 0)), ((1, 0), (2, 0))]
    assert list(find_rains.merge_consecutive_events(events)) == [
            (0, 0), (1, 0), (2, 0)]
    events = [((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0))]
    assert list(find_rains.merge_consecutive_events(events)) == [
            (0, 0), (1, 0), (2, 0), (3, 0)]


def test_iter_rains():
    assert list(find_rains.iter_rains(2, 1, [])) == []
    rain_data = [(0, 0), (1, 1)]
    assert list(find_rains.iter_rains(2, 1, rain_data)) == [
            [(0, 0), (1, 1)]]
    rain_data = [(0, 0), (1, 1), (2, 1)]
    assert list(find_rains.iter_rains(2, 1, rain_data)) == [
            [(0, 0), (1, 1), (2, 1)]]
    rain_data = [(0, 0), (1, 0), (2, 1), (3, 0), (4, 0), (5, 1)]
    assert list(find_rains.iter_rains(2, 1, rain_data)) == [
            [(1, 0), (2, 1), (3, 0)],
            [(4, 0), (5, 1)]]

