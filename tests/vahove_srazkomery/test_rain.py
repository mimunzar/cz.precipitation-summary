#!/usr/bin/env python3


import src.vahove_srazkomery.rain as rain


def test_iter_gt_periods():
    assert list(rain.iter_gt_periods(.9, 0, [])) == []
    data = [(0, 1)]
    assert list(rain.iter_gt_periods(.9, 1, data)) == [
            ((0, 1),)]
    data = [(0, 0), (1, 1)]
    assert list(rain.iter_gt_periods(.9, 2, data)) == [
            ((0, 0), (1, 1))]
    data = [(0, 0), (1, 1), (2, 1)]
    assert list(rain.iter_gt_periods(.9, 2, data)) == [
            ((0, 0), (1, 1)),
            ((1, 1), (2, 1))]


def test_iter_consecutive_events():
    assert list(rain.iter_consecutive_events([])) == []
    events = [((0, 0),)]
    assert list(rain.iter_consecutive_events(events)) == [
            [((0, 0),)]]
    events = [((0, 0),), ((1, 0),)]
    assert list(rain.iter_consecutive_events(events)) == [
            [((0, 0),), ((1, 0),)]]
    events = [((0, 0),), ((1, 0),), ((3, 0),), ((5, 0),), ((6, 0),)]
    assert list(rain.iter_consecutive_events(events)) == [
            [((0, 0),), ((1, 0),)],
            [((3, 0),)],
            [((5, 0),), ((6, 0),)]]


def test_merge_consecutive_events():
    assert list(rain.merge_consecutive_events([])) == []
    events = [((0, 0), (1, 0))]
    assert list(rain.merge_consecutive_events(events)) == [
            (0, 0), (1, 0)]
    events = [((0, 0), (1, 0)), ((1, 0), (2, 0))]
    assert list(rain.merge_consecutive_events(events)) == [
            (0, 0), (1, 0), (2, 0)]
    events = [((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0))]
    assert list(rain.merge_consecutive_events(events)) == [
            (0, 0), (1, 0), (2, 0), (3, 0)]


def test_iter_rains():
    assert list(rain.iter_rains(.9, 2, [])) == []
    data = [(0, 0), (1, 1)]
    assert list(rain.iter_rains(.9, 2, data)) == [
            ((0, 0), (1, 1))]
    data = [(0, 0), (1, 1), (2, 1)]
    assert list(rain.iter_rains(.9, 2, data)) == [
            ((0, 0), (1, 1), (2, 1))]
    data = [(0, 0), (1, 0), (2, 1), (3, 0), (4, 0), (5, 1)]
    assert list(rain.iter_rains(.9, 2, data)) == [
            ((1, 0), (2, 1), (3, 0)),
            ((4, 0), (5, 1))]


def test_is_heavy():
    pass

