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


def iter_consecutive_events(events_it):
    ordering = lambda e: e[0] - e[1][0][0]
    groups   = it.groupby(enumerate(events_it), key=ordering)
    #^ Group by an index and a first event's index
    return (tuple(map(op.itemgetter(1), g)) for _, g in groups)


def merge_consecutive_events(events_it):
    chained_events = it.chain.from_iterable(events_it)
    events_by_time = sorted(chained_events, key=op.itemgetter(0))
    return util.dedupe(events_by_time)


def trim_event(data_it):
    doesnt_rain = lambda e: not e[1]
    trim_start  = lambda i: tuple(it.dropwhile(doesnt_rain, i))
    return reversed(trim_start(reversed(trim_start(data_it))))


def make_data_utc_date():
    delta_10m = dt.timedelta(minutes=10)
    epoch_10m = (dt.datetime(2010, 1, 1) - dt.datetime(1970, 1, 1))//delta_10m
    utc_date  = lambda secs: dt.datetime.fromtimestamp(secs, dt.timezone.utc)
    return lambda d: utc_date((epoch_10m + d[0])*delta_10m.seconds)


def iter_events(amount, period, data_it):
    rain_events  = iter_gt_periods(amount, period, data_it)
    consecutives = iter_consecutive_events(rain_events)
    return map(lambda c: trim_event(merge_consecutive_events(c)), consecutives)


TO_UTC_DATE = make_data_utc_date()


def iter_rains(amount, period, data_it, fn_data_date=TO_UTC_DATE):
    events_it = iter_events(amount, period, data_it)
    add_date  = lambda d: (d[0], d[1], fn_data_date(d))
    return map(lambda e: tuple(map(add_date, e)), events_it)


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


EVENT_YEAR  = lambda e: TO_UTC_DATE(e[0]).year
EVENT_MONTH = lambda e: TO_UTC_DATE(e[0]).month


def iter_yearly(events_it, fn_event_year=EVENT_YEAR):
    grouped  = it.groupby(events_it, key=fn_event_year)
    years    = cl.defaultdict(tuple, {k: tuple(l) for k, l in grouped})
    return ((y, years[y]) for y in range(2010, 2021))


def iter_monthly(events_it, fn_event_month=EVENT_MONTH):
    by_month = sorted(events_it, key=fn_event_month)
    grouped  = it.groupby(by_month, key=fn_event_month)
    months   = cl.defaultdict(tuple, {k: tuple(l) for k, l in grouped})
    return ((m, months[m]) for m in range(1, 13))

