#!/usr/bin/env python3

import src.precipitation_summary.rain as rain


def test_apply_sum():
    assert rain.apply_sum(lambda x: x, tuple()) == 0
    assert rain.apply_sum(lambda x: x, ((0, 1),)) == 1
    assert rain.apply_sum(lambda x: x, ((0, 1), (1, 2))) == 3
    assert rain.apply_sum(lambda x: x + 1, ((0, 1), (1, 2))) == 5


def test_max_period():
    assert rain.max_period(1, tuple()) == ()
    assert rain.max_period(1, ((0, 1),)) == ((0, 1),)
    assert rain.max_period(1, ((0, 1), (1, 2),)) == ((1, 2),)
    assert rain.max_period(2, ((0, 1), (1, 2), (2, 3))) == ((1, 2), (2, 3),)


def test_iter_gt_periods():
    assert list(rain.iter_gt_periods(.9, 0, [])) == []
    data = [(0, 1)]
    assert list(rain.iter_gt_periods(.9, 1, data)) == [
            ((0, 1),)]
    data = [(0, 0), (1, 1)]
    assert list(rain.iter_gt_periods(.9, 2, data)) == [
            ((0, 0), (1, 1),)]
    data = [(0, 0), (1, 1), (2, 1)]
    assert list(rain.iter_gt_periods(.9, 2, data)) == [
            ((0, 0), (1, 1),),
            ((1, 1), (2, 1),)]


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


def test_trim_event():
    assert list(rain.trim_event(((0, 0),))) == []
    assert list(rain.trim_event(((0, 1), (1, 0)))) == [(0, 1)]
    assert list(rain.trim_event(((0, 1), (1, 0), (2, 0)))) == [(0, 1)]
    assert list(rain.trim_event(((0, 1), (1, 0), (2, 1)))) == [(0, 1), (1, 0), (2, 1)]


def test_iter_rains():
    assert list(rain.iter_rains(.9, 2, [])) == []
    data = [(0, 0), (1, 1)]
    assert list(rain.iter_rains(.9, 2, data)) == [
            ((1, 1),)]
    data = [(0, 0), (1, 1), (2, 1)]
    assert list(rain.iter_rains(.9, 2, data)) == [
            ((1, 1), (2, 1),)]
    data = [(0, 0), (1, 1), (2, 1), (3, 0), (4, 0), (5, 1)]
    assert list(rain.iter_rains(.9, 2, data)) == [
            ((1, 1), (2, 1),),
            ((5, 1),)]

