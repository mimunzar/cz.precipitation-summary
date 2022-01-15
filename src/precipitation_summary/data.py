#!/usr/bin/env python3

import collections as cl
import datetime    as dt
import itertools   as it
import functools   as ft

import openpyxl as xl

import src.precipitation_summary.rain as rain
import src.precipitation_summary.util as util


def parse_data(rain_row_it):
    result    = cl.defaultdict(list)
    cell_val  = lambda c: c.value or 0
    is_outage = lambda c: c.value == None
    for r in rain_row_it:
        for c in r:
            val = (cell_val(c), is_outage(c))
            result[c.column_letter].append(val)
    return result


def iter_parsed(parsed):
    vals    = it.chain.from_iterable(parsed[k] for k in sorted(parsed.keys()))
    flatten = lambda i: tuple(util.value_chain(i))
    return map(flatten, enumerate(vals))


def from_sheet(fpath):
    workbook  = xl.load_workbook(filename=fpath)
    worksheet = workbook.worksheets[0]
    data_it   = map(ft.partial(util.drop, 4), util.drop(4, worksheet.iter_rows()))
    return (worksheet['A1'].value, iter_parsed(parse_data(data_it)))


def make_formatter(fields, fn_time):
    delta  = dt.timedelta(minutes=10)
    offset = int((dt.datetime(2010, 1, 1) - dt.datetime(1970, 1, 1))/delta)
    def formatter(idx, val):
        d = dt.datetime.fromtimestamp((offset + fn_time(val))*delta.seconds)
        return tuple(fn(idx, d, val) for fn in fields.values())
    return formatter


def make_cell(worksheet, val, style={}):
    cell       = xl.cell.Cell(worksheet)
    cell.value = val
    for k, v in style.items():
        setattr(cell, k, v)
    return cell


def write_sheet_header(worksheet, station, labels):
    font_setting = xl.styles.Font(name='Calibri', bold=True)
    val_in_bold  = lambda x: make_cell(worksheet, x, style={'font': font_setting})
    row_in_bold  = lambda i: list(map(val_in_bold, i))
    worksheet.append(row_in_bold([station]))
    worksheet.append(row_in_bold(labels))


def write_sheet_data(worksheet, fn_event_to_rows, event_it):
    left          = xl.styles.Alignment(horizontal='left')
    fill          = lambda c: xl.styles.PatternFill('solid', fgColor=c)
    val_with_fill = lambda f, x: make_cell(worksheet, x,style={'fill': f, 'alignment': left})
    row_with_fill = lambda f, i: [val_with_fill(f, x) for x in i]
    fill_event_it = zip(it.cycle([fill('d5f5c6'), fill('f2c9a3')]), event_it)
    for i, (fill, event) in enumerate(fill_event_it, start=1):
        for row in fn_event_to_rows(i, event):
            worksheet.append(row_with_fill(fill, row))


def hr_list(worksheet, station, event_it):
    fields = cl.OrderedDict({
        'id'                 : lambda i, _, __: i,
        'datum [YYYY-MM-DD]' : lambda _, d, __: f'{d.year:04}-{d.month:02}-{d.day:02}',
        'rok'                : lambda _, d, __: d.year,
        'měsíc'              : lambda _, d, __: d.month,
        'den'                : lambda _, d, __: d.day,
        'termín [HH:MM]'     : lambda _, d, __: f'{d.hour:02}:{d.minute:02}',
        'SRA10M [mm/10min.]' : lambda _, __, r: r[1],
        'kin. energie [J]'   : lambda _, __, r: round(rain.kinetic_energy(r[1]), 4),
    })
    write_sheet_header(worksheet, station, fields.keys())
    formatter     = make_formatter(fields, lambda v: v[0])
    event_to_rows = lambda i, e: (formatter(i, v) for v in e)
    write_sheet_data(worksheet, event_to_rows, event_it)


def heavy_rain_stat_list(worksheet, station, event_it):
    fields = cl.OrderedDict({
        'id'                 : lambda i, _, __: i,
        'datum [YYYY-MM-DD]' : lambda _, d, __: f'{d.year:04}-{d.month:02}-{d.day:02}',
        'rok'                : lambda _, d, __: d.year,
        'měsíc'              : lambda _, d, __: d.month,
        'den'                : lambda _, d, __: d.day,
        'doba trvání [hod]'  : lambda _, __, e: \
                round((len(e)*dt.timedelta(minutes=10))/dt.timedelta(hours=1), 2),
        'celkový úhrn [mm]'  : lambda _, __, e: \
                round(rain.total_amount(e), 2),
        '20 min. max. [mm]'  : lambda _, __, e: \
                round(rain.total_max_period(util.minutes(20), e), 2),
        '30 min. max. [mm]'  : lambda _, __, e: \
                round(rain.total_max_period(util.minutes(30), e), 2),
        'kin. energie [MJ]'  : lambda _, __, e: \
                round(rain.total_kinetic_energy(e), 4),
        'erozivita [R]'      : lambda _, __, e: \
                round(rain.total_erosivity(util.minutes(30), e), 4),
    })
    write_sheet_header(worksheet, station, fields.keys())
    formatter     = make_formatter(fields, lambda e: e[0][0])
    event_to_rows = lambda i, e: [formatter(i, e)]
    write_sheet_data(worksheet, event_to_rows, event_it)


def to_sheet(fpath, station, event_it):
    event_it       = tuple(event_it)
    workbook       = xl.Workbook()
    hr_sheet       = workbook.active
    hr_sheet.title = 'heavy_rains'
    hr_list(hr_sheet, station, event_it)

    hr_stat_sheet       = workbook.create_sheet()
    hr_stat_sheet.title = 'heavy_rains_stats'
    heavy_rain_stat_list(hr_stat_sheet, station, event_it)
    workbook.save(fpath)

