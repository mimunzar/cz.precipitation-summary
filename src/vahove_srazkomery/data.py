#!/usr/bin/env python3

from openpyxl import load_workbook

import collections as cl
import itertools   as it


def iter_rain_row(fpath):
    work_book  = load_workbook(filename=fpath, read_only=True)
    work_sheet = work_book.worksheets[0]
    rain_cols  = lambda r: it.islice(r, 4, None)
    return map(rain_cols, it.islice(work_sheet.iter_rows(), 4, None))


def iter_rain_data(rain_row_it):
    vals_by_col = cl.defaultdict(list)
    for r in rain_row_it:
        for c in r:
            vals_by_col[c.column_letter].append(c.value or 0)
    col_vals = (vals_by_col[k] for k in sorted(vals_by_col.keys()))
    return enumerate(it.chain.from_iterable(col_vals))

