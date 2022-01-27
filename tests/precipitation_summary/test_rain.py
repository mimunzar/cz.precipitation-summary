#!/usr/bin/env python3

import itertools as it
import datetime  as dt
import operator  as op

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


def test_total_max_period():
    assert rain.total_max_period(1, tuple()) == 0
    assert rain.total_max_period(1, ((0, 1),)) == 1
    assert rain.total_max_period(1, ((0, 1), (1, 2),)) == 2
    assert rain.total_max_period(2, ((0, 1), (1, 2), (2, 3))) == 5


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
            (((0, 0),),)]
    events = [((0, 0),), ((1, 0),)]
    assert list(rain.iter_consecutive_events(events)) == [
            (((0, 0),), ((1, 0),),)]
    events = [((0, 0),), ((1, 0),), ((3, 0),), ((5, 0),), ((6, 0),)]
    assert list(rain.iter_consecutive_events(events)) == [
            (((0, 0),), ((1, 0),),),
            (((3, 0),),),
            (((5, 0),), ((6, 0),),)]


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
    to_data_date = lambda d: d[0]
    data = []
    assert list(rain.iter_rains(.9, 2, data, to_data_date)) == []
    data = [(0, 0), (1, 1)]
    assert list(rain.iter_rains(.9, 2, data, to_data_date)) == [
            ((1, 1, 1),)]
    data = [(0, 0), (1, 1), (2, 1)]
    assert list(rain.iter_rains(.9, 2, data, to_data_date)) == [
            ((1, 1, 1), (2, 1, 2),)]
    data = [(0, 0), (1, 1), (2, 1), (3, 0), (4, 0), (5, 1)]
    assert list(rain.iter_rains(.9, 2, data, to_data_date)) == [
            ((1, 1, 1), (2, 1, 2),),
            ((5, 1, 5),)]


def test_is_mild_rain():
    assert rain.is_mid_rain(()) == False
    assert rain.is_mid_rain(it.islice(it.repeat((0, 3)), 4)) == False
    assert rain.is_mid_rain(it.islice(it.repeat((0, 3)), 5)) == True
    #^ The amount is higher than 12.5 mm in total
    assert rain.is_mid_rain(it.islice(it.repeat((0, 5)), 1)) == False
    assert rain.is_mid_rain(it.islice(it.repeat((0, 5)), 2)) == True
    #^ The amount per 20 minutes is than 8.3 mm


def test_is_heavy_rain():
    assert rain.is_heavy_rain(()) == False
    assert rain.is_heavy_rain(it.islice(it.repeat((0, 3)), 4)) == False
    assert rain.is_heavy_rain(it.islice(it.repeat((0, 5)), 2)) == False
    assert rain.is_heavy_rain(it.islice(it.repeat((0, 5)), 3)) == True
    #^ The amount is higher than 12.5 mm in total and the amount per 20 minutes
    # is more than 8.3 mm


def test_make_data_utc_date():
    data_to_date = rain.make_data_utc_date()
    assert data_to_date((0,)) == dt.datetime(2010, 1, 1, 0,  0, tzinfo=dt.timezone.utc)
    assert data_to_date((1,)) == dt.datetime(2010, 1, 1, 0, 10, tzinfo=dt.timezone.utc)
    assert data_to_date((2,)) == dt.datetime(2010, 1, 1, 0, 20, tzinfo=dt.timezone.utc)


def test_iter_yearly():
    data   = []
    result = list(rain.iter_yearly(data, fn_event_year=lambda e: e[0][0]))
    assert list(map(op.itemgetter(0), result)) == list(range(2010, 2021))
    assert all(map(lambda y: 0 == len(y), map(op.itemgetter(1), result)))

    data   = [((2010,), (2011,)), ((2011,),)]
    result = list(rain.iter_yearly(data, fn_event_year=lambda e: e[0][0]))
    assert result[0] == (2010, (((2010,), ((2011,))),))
    #^ The aggregation is done by the first element in events
    assert result[1] == (2011, (((2011,),),))
    assert result[2] == (2012, tuple())
    assert all(map(lambda y: 0 == len(y), map(op.itemgetter(1), result[3:])))


def test_iter_monthly():
    data   = []
    result = list(rain.iter_monthly(data, fn_event_month=lambda e: e[0][0]))
    assert len(result) == 0

    data = [(2010, (((1,), ((2,))),))]
    result = list(rain.iter_monthly(data, fn_event_month=lambda e: e[0][0]))
    assert len(result) == 12
    assert result[0] == (2010, 1, (((1,), (2,)),))
    #^ The aggregation is done by the first element in events
    assert all(map(lambda m: 0 == len(m[2]), result[1:]))

    data = [
        (2010, (((1,), ((2,))),)),
        (2011, (((1,),),)),
    ]
    result = list(rain.iter_monthly(data, fn_event_month=lambda e: e[0][0]))
    assert len(result) == 24
    assert result[0] == (2010, 1, (((1,), (2,)),))
    assert all(map(lambda m: 0 == len(m[2]), result[1:12]))
    assert result[12] == (2011, 1, (((1,),),))
    assert all(map(lambda m: 0 == len(m[2]), result[13:]))

