#!/usr/bin/env python3

import src.vahove_srazkomery.data as data
import src.vahove_srazkomery.rain as rain


def minutes(n):
    return n//10


def is_heavy_rain(data_it):
    period_of_gt_rain = list(rain.iter_gt_periods(8.3, minutes(20), data_it))
    exceeded_amount   = 12.5 < rain.total_amount(data_it)
    return exceeded_amount or period_of_gt_rain


def iter_heavy_rains(data_it):
    hours    = lambda n: n*minutes(60)
    rains_it = rain.iter_rains(1.27, hours(6), data_it)
    return filter(is_heavy_rain, rains_it)


if __name__ == '__main__':
    file = '.git/VAHOVE_SRAZKOMERY/data_cast_1/B1HOLE01_SRA10M.xlsx'
    station, data_it = data.from_file(file)
    data.write_rain_sheet('sample.xlsx', station, iter_heavy_rains(data_it))

