#!/usr/bin/env python3

from openpyxl import load_workbook

import collections as cl
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
    work_book  = load_workbook(filename=fpath, read_only=True)
    work_sheet = work_book.worksheets[0]
    return iter_rain_rows_data(iter_rain_rows(work_sheet.iter_rows()))

