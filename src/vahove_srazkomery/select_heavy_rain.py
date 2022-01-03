#!/usr/bin/env python3

import argparse
import os
import sys

import src.vahove_srazkomery.data as data
import src.vahove_srazkomery.rain as rain


def parse_args(args_it):
    parser = argparse.ArgumentParser(
            description='Allows to create statistics about heavy rains')
    parser.add_argument('-i', '--input_dir',
            required=True, help='The director which contains measurement files')
    parser.add_argument('-o', '--output_dir',
            required=True, help='The director which will contain statistic files')
    parsed = vars(parser.parse_args(args_it))
    return (parsed['input_dir'], parsed['output_dir'])


def iter_input_filenames(i_dir):
    is_excel_file = lambda s: s.endswith('.xlsx')
    return filter(is_excel_file, os.listdir(i_dir))


def output_filename(filename):
    path, extension = os.path.splitext(filename)
    return f'{path}.stat{extension}'


def iter_input_output_files(i_dir, o_dir):
    input_path  = lambda s: os.path.join(i_dir, s)
    output_path = lambda s: os.path.join(o_dir, output_filename(s))
    return ((input_path(n), output_path(n)) for n in iter_input_filenames(i_dir))


def is_heavy_rain(data_it):
    period_of_gt_rain = list(rain.iter_gt_periods(8.3, data.minutes(20), data_it))
    exceeded_amount   = 12.5 < rain.total_amount(data_it)
    return exceeded_amount or period_of_gt_rain


def iter_heavy_rains(data_it):
    hours    = lambda n: n*data.minutes(60)
    rains_it = rain.iter_rains(1.27, hours(6), data_it)
    return filter(is_heavy_rain, rains_it)


if __name__ == '__main__':
    i_dir, o_dir = parse_args(sys.argv[1:])
    os.makedirs(o_dir, exist_ok=True)
    for i_path, o_path in iter_input_output_files(i_dir, o_dir):
        station, data_it = data.from_file(i_path)
        data.write_rain_sheet(o_path, station, iter_heavy_rains(data_it))

