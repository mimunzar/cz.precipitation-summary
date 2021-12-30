#!/usr/bin/env python3

import itertools as it
import operator  as op

import src.vahove_srazkomery.util as util


def total_amount(data_it):
    return sum(map(op.itemgetter(1), data_it))


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


def iter_rains(amount, period, data_it):
    rain_events  = iter_gt_periods(amount, period, data_it)
    consecutives = iter_consecutive_events(rain_events)
    return (tuple(merge_consecutive_events(c)) for c in consecutives)

