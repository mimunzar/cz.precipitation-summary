#!/usr/bin/env python3

import openpyxl as xl

import collections as cl
import datetime    as dt
import functools   as ft
import itertools   as it


def iter_rain_rows(rows_it):
    rain_cols = lambda r: it.islice(r, 4, None)
    return map(rain_cols, it.islice(rows_it, 4, None))


def iter_rain_rows_data(rain_row_it):
    col_vals = cl.defaultdict(list)
    for r in rain_row_it:
        for c in r:
            col_vals[c.column_letter].append(c.value or 0)
    joined_cols = (col_vals[k] for k in sorted(col_vals.keys()))
    return enumerate(it.chain.from_iterable(joined_cols))


def from_file(fpath):
    wb = xl.load_workbook(filename=fpath, read_only=True)
    ws = wb.worksheets[0]
    iter_data  = iter_rain_rows_data(iter_rain_rows(ws.iter_rows()))
    return (ws['A1'].value, iter_data)


def make_formatter(dt_offset):
    delta  = dt.timedelta(minutes=10)
    offset = int((dt_offset - dt.datetime(1970, 1, 1))/delta)
    header = ['id', 'rok', 'měsíc', 'den', 'termín', 'SRA10M']
    def formatter(idx, rain_val):
        t, x = rain_val
        d    = dt.datetime.fromtimestamp((offset + t)*delta.seconds)
        return [idx, d.year, d.month, d.day, f'{d.hour:02}:{d.minute:02}', x]
    return (header, formatter)


def make_cell(ws, val, style={}):
    c       = xl.cell.Cell(ws)
    c.value = val
    for k, v in style.items():
        setattr(c, k, v)
    return c


def write_selected_events(station, ws, event_it):
    header, formatter = make_formatter(dt.datetime(2010, 1, 1))
    bold              = xl.styles.Font(name='Calibri', bold=True)
    ws.append(list(map(ft.partial(make_cell, ws, style={'font': bold}), [station])))
    ws.append(list(map(ft.partial(make_cell, ws, style={'font': bold}), header)))

    left = xl.styles.Alignment(horizontal='left')
    fill = lambda c: xl.styles.PatternFill('solid', fgColor=c)
    cell_fill_1 = ft.partial(make_cell, ws, style={'fill': fill('d5f5c6'), 'alignment': left})
    cell_fill_2 = ft.partial(make_cell, ws, style={'fill': fill('f2c9a3'), 'alignment': left})
    for i, event in enumerate(event_it, start=1):
        for val in event:
            cell_fill = cell_fill_1 if i % 2 else cell_fill_2
            ws.append(list(map(cell_fill, formatter(i, val))))


def write_rain_sheet(fpath, station, event_it):
    wb = xl.Workbook()
    ws = wb.active
    ws.title = 'selected_events'
    write_selected_events(station, ws, event_it)
    wb.save(fpath)

