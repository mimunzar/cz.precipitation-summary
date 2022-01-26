#!/usr/bin/env python3

import itertools   as it
import collections as cl
import datetime    as dt
import math        as ma
import operator    as op

import src.precipitation_summary.util as util


def apply_sum(f, data_it):
    return sum(map(f, map(op.itemgetter(1), data_it)))


def total_amount(data_it):
    return apply_sum(lambda x: x, data_it)


def kinetic_energy(amount_10m):
    return amount_10m*(0.29*(1 - 0.72*ma.exp(-0.05*amount_10m)))


def total_kinetic_energy(data_it):
    return apply_sum(kinetic_energy, data_it)


def max_period(period, data_it):
    events = util.sliding_window(period, data_it)
    return max(events, key=total_amount, default=tuple())


def total_max_period(period, data_it):
    return total_amount(max_period(period, data_it))


def total_erosivity(period, data_it):
    return 2*total_max_period(period, data_it)*total_kinetic_energy(data_it)


def iter_gt_periods(amount, period, data_it):
    events           = util.sliding_window(period, data_it)
    has_total_amount = lambda e: amount < total_amount(e)
    return filter(has_total_amount, events)


def iter_consecutive_events(fn_order, events_it):
    ordering = lambda ie: ie[0] - fn_order(ie[1])
    groups   = it.groupby(enumerate(events_it), key=ordering)
    return (tuple(map(op.itemgetter(1), g)) for _, g in groups)


def merge_consecutive_events(events_it):
    chained_events = it.chain.from_iterable(events_it)
    events_by_time = sorted(chained_events, key=op.itemgetter(0))
    return util.dedupe(events_by_time)


def trim_event(data_it):
    doesnt_rain = lambda e: not e[1]
    trim_start  = lambda i: tuple(it.dropwhile(doesnt_rain, i))
    return reversed(trim_start(reversed(trim_start(data_it))))


def iter_rains(amount, period, data_it):
    rain_events  = iter_gt_periods(amount, period, data_it)
    consecutives = iter_consecutive_events(lambda e: e[0][0], rain_events)
    #^ Group by an index and a first event's index
    return (tuple(trim_event(merge_consecutive_events(c))) for c in consecutives)


def is_mid_rain(data_it):
    data_it         = tuple(data_it)
    intense_period  = 0 < len(tuple(iter_gt_periods(8.3, util.minutes(20), data_it)))
    exceeded_amount = 12.5 < total_amount(data_it)
    return exceeded_amount or intense_period


def is_heavy_rain(data_it):
    data_it         = tuple(data_it)
    intense_period  = 0 < len(tuple(iter_gt_periods(8.3, util.minutes(20), data_it)))
    exceeded_amount = 12.5 < total_amount(data_it)
    return exceeded_amount and intense_period


def make_data_utc_date():
    delta_10m = dt.timedelta(minutes=10)
    epoch_10m = (dt.datetime(2010, 1, 1) - dt.datetime(1970, 1, 1))//delta_10m
    cest_date = lambda secs: dt.datetime.fromtimestamp(secs, dt.timezone.utc)
    return lambda d: cest_date((epoch_10m + d[0])*delta_10m.seconds)


TO_UTC_DATE    = make_data_utc_date()
GET_DATA_YEAR  = lambda d: TO_UTC_DATE(d).year
GET_DATA_MONTH = lambda d: TO_UTC_DATE(d).month


def iter_yearly(events_it, fn_year=GET_DATA_YEAR):
    grouped     = it.groupby(util.flatten(events_it), key=fn_year)
    year        = cl.defaultdict(tuple, {k: tuple(l) for k, l in grouped})
    iter_events = lambda it: iter_consecutive_events(lambda e: e[0], it)
    return ((y, tuple(iter_events(year[y]))) for y in range(2010, 2021))


def iter_monthly(yearly_it, fn_month=GET_DATA_MONTH):
    iter_events = lambda it: iter_consecutive_events(lambda e: e[0], it)
    def montly(yearly):
        y, event_it = yearly
        grouped     = it.groupby(util.flatten(event_it), key=fn_month)
        month       = cl.defaultdict(tuple, {k: tuple(l) for k, l in grouped})
        return ((y, m, tuple(iter_events(month[m]))) for m in range(1, 13))
    return util.flatten(map(montly, yearly_it))

