#!/usr/bin/env python3

import argparse
import functools as ft
import os
import sys

import src.precipitation_summary.data as data
import src.precipitation_summary.rain as rain
import src.precipitation_summary.util as util


def parse_args(args_it):
    parser = argparse.ArgumentParser(
            description='Allows to create statistics about heavy rains')
    parser.add_argument('-i', '--input_dir',
            required=True, help='The directory which contains measurement files')
    parser.add_argument('-o', '--output_dir',
            required=True, help='The directory which will contain statistic files')
    parsed = vars(parser.parse_args(args_it))
    return (parsed['input_dir'], parsed['output_dir'])


def iter_input_filenames(i_dir):
    is_excel_file = lambda s: s.endswith('.xlsx')
    return filter(is_excel_file, os.listdir(i_dir))


def output_filename(filename):
    path, extension = os.path.splitext(filename)
    return f'{path}.stat{extension}'


def iter_pending_files(i_dir, o_dir):
    input_path  = lambda s: os.path.join(i_dir, s)
    output_path = lambda s: os.path.join(o_dir, output_filename(s))
    input_files = list(iter_input_filenames(i_dir))
    total_files = len(input_files)
    return ((input_path(f), output_path(f), total_files) for f in input_files)


def process_directory(i_dir, o_dir):
    to_station_workbook = data.to_station_workbook
    to_stat_workbook    = data.make_to_stat_workbook(os.path.join(o_dir, 'stat.xlsx'))
    def process_file(done, pending_files_it):
        i_path, o_path, total = pending_files_it
        current_file = os.path.basename(i_path)
        progress_bar = lambda done: util.print_progress(40, total, done)
        print(f'{progress_bar(done)} ({current_file})', end='\r')

        station, data_it = data.from_workbook(i_path)
        rains_it         = tuple(rain.iter_rains(1.27, util.hours(6), data_it))
        heavy_rains_it   = tuple(filter(rain.is_heavy_rain, rains_it))
        to_station_workbook(o_path, station, rains_it, heavy_rains_it)
        done += 1
        to_stat_workbook(done, station, rains_it, heavy_rains_it)
        print(f'{progress_bar(done)} ({current_file})', end='\r')
        return done
    return ft.reduce(process_file, iter_pending_files(i_dir, o_dir), 0)


if __name__ == '__main__':
    i_dir, o_dir = parse_args(sys.argv[1:])
    os.makedirs(o_dir, exist_ok=True)
    process_directory(i_dir, o_dir)
    print()

