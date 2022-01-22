#!/usr/bin/env python3

import itertools as it
import math      as ma
import operator  as op

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
    by_ordering = lambda ie: ie[0] - ie[1][0][0]
    #^ Group by an index and a first event's index
    groups      = it.groupby(enumerate(events_it), key=by_ordering)
    return (list(map(op.itemgetter(1), g)) for _, g in groups)


def merge_consecutive_events(events_it):
    chained_events = it.chain.from_iterable(events_it)
    events_by_time = sorted(chained_events, key=op.itemgetter(0))
    return util.dedupe(events_by_time)


def trim_event(data_it):
    doesnt_rain = lambda e: not e[1]
    trim_start  = lambda i: list(it.dropwhile(doesnt_rain, i))
    return reversed(trim_start(reversed(trim_start(data_it))))


def iter_rains(amount, period, data_it):
    rain_events  = iter_gt_periods(amount, period, data_it)
    consecutives = iter_consecutive_events(rain_events)
    return (tuple(trim_event(merge_consecutive_events(c))) for c in consecutives)


def is_heavy_rain(data_it):
    data_it         = tuple(data_it)
    intense_period  = 0 < len(tuple(iter_gt_periods(8.3, util.minutes(20), data_it)))
    exceeded_amount = 12.5 < total_amount(data_it)
    return exceeded_amount or intense_period
