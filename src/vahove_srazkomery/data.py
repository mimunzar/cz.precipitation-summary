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
    col_data = cl.defaultdict(list)
    for r in rain_row_it:
        for c in r:
            col_data[c.column_letter].append(c.value or 0)
    return it.chain.from_iterable(col_data[k] for k in sorted(col_data.keys()))


if __name__ == '__main__':
    file = '.git/VAHOVE_SRAZKOMERY/data_cast_1/B1HOLE01_SRA10M.xlsx'
    data = iter_rain_data(iter_rain_row(file))

