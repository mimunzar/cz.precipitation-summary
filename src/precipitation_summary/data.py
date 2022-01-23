#!/usr/bin/env python3

import collections as cl
import datetime    as dt
import itertools   as it
import functools   as ft

import openpyxl       as xl
import openpyxl.utils as xl_utils

import src.precipitation_summary.rain as rain
import src.precipitation_summary.util as util


LEFT_ALIGN = xl.styles.Alignment(horizontal='left')


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


def from_workbook(fpath):
    workbook  = xl.load_workbook(filename=fpath)
    worksheet = workbook.active
    data_it   = map(ft.partial(util.drop, 4), util.drop(4, worksheet.iter_rows()))
    return (worksheet['A1'].value, iter_parsed(parse_data(data_it)))


def make_station_formatter(fields, fn_start_time):
    delta  = dt.timedelta(minutes=10)
    offset = int((dt.datetime(2010, 1, 1) - dt.datetime(1970, 1, 1))/delta)
    def formatter(idx, val):
        d = dt.datetime.fromtimestamp((offset + fn_start_time(val))*delta.seconds)
        return (fn(idx, d, val) for fn in fields.values())
    return formatter


def make_cell(worksheet, val, style={}):
    cell       = xl.cell.Cell(worksheet)
    cell.value = val
    for k, v in style.items():
        setattr(cell, k, v)
    return cell


def set_column_width(worksheet, labels_it):
    cl_it = map(xl_utils.get_column_letter, it.count(1))
    for c, l in zip(cl_it, labels_it):
        worksheet.column_dimensions[c].width = max(10, 1.23*len(str(l)))


def write_sheet_labels(worksheet, labels_it):
    font_setting = xl.styles.Font(name='Calibri', bold=True)
    val_in_bold  = lambda x: make_cell(worksheet, x, style={'font': font_setting})
    row_in_bold  = lambda i: list(map(val_in_bold, i))
    worksheet.append(row_in_bold(labels_it))
    set_column_width(worksheet, labels_it)


def make_fill(color):
    return xl.styles.PatternFill('solid', fgColor=color)


def write_sheet_data(worksheet, fn_iter_row_vals, event_it):
    style   = lambda fill: {'fill': fill, 'alignment': LEFT_ALIGN}
    cell    = lambda fill, x: make_cell(worksheet, x, style(fill))
    fill_it = it.cycle((make_fill('d5f5c6'), make_fill('f2c9a3')))
    for i, (fill, event) in enumerate(zip(fill_it, event_it), start=1):
        for val_it in fn_iter_row_vals(i, event):
            worksheet.append(tuple(map(ft.partial(cell, fill), val_it)))


def write_timeline_sheet(worksheet, station, event_it):
    fields = cl.OrderedDict({
        'id'                 : lambda i, _, __: i,
        'datum [YYYY-MM-DD]' : lambda _, d, __: f'{d.year:04}-{d.month:02}-{d.day:02}',
        'rok'                : lambda _, d, __: d.year,
        'měsíc'              : lambda _, d, __: d.month,
        'den'                : lambda _, d, __: d.day,
        'termín [HH:MM]'     : lambda _, d, __: f'{d.hour:02}:{d.minute:02}',
        'SRA10M [mm/10min.]' : lambda _, __, r: r[1],
    })
    write_sheet_labels(worksheet, [station])
    write_sheet_labels(worksheet, fields.keys())
    formatter   = make_station_formatter(fields, lambda v: v[0])
    iter_sra10m = lambda idx, event_it: (formatter(idx, v) for v in event_it)
    write_sheet_data(worksheet, iter_sra10m, event_it)


def write_param_sheet(worksheet, station, event_it):
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
    write_sheet_labels(worksheet, [station])
    write_sheet_labels(worksheet, fields.keys())
    formatter   = make_station_formatter(fields, lambda e: e[0][0])
    iter_events = lambda idx, event_it: [formatter(idx, event_it)]
    write_sheet_data(worksheet, iter_events, event_it)


def write_station_workbook(workbook, name, station, event_it):
    event_it             = tuple(event_it)
    timeline_sheet       = workbook.create_sheet()
    timeline_sheet.title = name
    write_timeline_sheet(timeline_sheet, station, event_it)

    param_sheet       = workbook.create_sheet()
    param_sheet.title = f'{name}_params'
    write_param_sheet(param_sheet, station, event_it)


def to_station_workbook(fpath, station, event_it, heavy_event_it):
    workbook = xl.Workbook()
    workbook.remove(workbook.active)
    write_station_workbook(workbook, 'rain', station, event_it)
    write_station_workbook(workbook, 'heavy_rain', station, heavy_event_it)
    workbook.save(fpath)


def make_append_stat_sheet(worksheet):
    fields = cl.OrderedDict({
        'id'                     : lambda i, _, __: i,
        'stanice'                : lambda _, s, __: s,
        'počet srážek'           : lambda _, __, e: len(e),
        'suma SRA10M [mm/10let]' : lambda _, __, e: round(sum(map(rain.total_amount, e)), 2),
    })
    write_sheet_labels(worksheet, fields.keys())
    fill_it = it.cycle((make_fill('d5f5c6'), make_fill('f2c9a3')))
    def append_stat_sheet(idx, station, event_it):
        style = {'alignment': LEFT_ALIGN, 'fill': next(fill_it)}
        vals  = map(lambda fn: fn(idx, station, event_it), fields.values())
        cell  = lambda v: make_cell(worksheet, v, style)
        worksheet.append(tuple(map(cell, vals)))
    return append_stat_sheet


def make_append_stat_workbook(workbook, name):
    stat_sheet        = workbook.create_sheet()
    stat_sheet.title  = name
    append_stat_sheet = make_append_stat_sheet(stat_sheet)
    return append_stat_sheet


def make_to_stat_workbook(fpath):
    workbook          = xl.Workbook()
    workbook.remove(workbook.active)
    append_rain       = make_append_stat_workbook(workbook, 'rain')
    append_heavy_rain = make_append_stat_workbook(workbook, 'heavy_rain')
    def to_stat_workbook(idx, station, event_it, heavy_event_it):
        append_rain      (idx, station, event_it)
        append_heavy_rain(idx, station, heavy_event_it)
        workbook.save(fpath)
    return to_stat_workbook

