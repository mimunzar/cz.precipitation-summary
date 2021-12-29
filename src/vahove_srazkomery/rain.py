#!/usr/bin/env python3

import itertools as it
import operator  as op

import src.vahove_srazkomery.util as util



def iter_rain_events(period, threshold, rain_data_it):
    events         = util.sliding_window(period, rain_data_it)
    event_values   = lambda e: map(op.itemgetter(1), e)
    raining_events = lambda e: threshold <= sum(event_values(e))
    return filter(raining_events, events)


def iter_consecutive_events(rain_events_it):
    by_ordering = lambda ie: ie[0] - ie[1][0][0]
    #^ Group by an index and a first event's index
    groups      = it.groupby(enumerate(rain_events_it), key=by_ordering)
    return (list(map(op.itemgetter(1), g)) for _, g in groups)


def merge_consecutive_events(rain_events_it):
    chained_events = it.chain.from_iterable(rain_events_it)
    events_by_time = sorted(chained_events, key=op.itemgetter(0))
    return util.dedupe(events_by_time)


def iter_rains(period, threshold, rain_data_it):
    rain_events  = iter_rain_events(period, threshold, rain_data_it)
    consecutives = iter_consecutive_events(rain_events)
    return (list(merge_consecutive_events(c)) for c in consecutives)

