#!/usr/bin/env python3

import src.vahove_srazkomery.data as data
import src.vahove_srazkomery.rain as rain


if __name__ == '__main__':
    file = '.git/VAHOVE_SRAZKOMERY/data_cast_1/B1HOLE01_SRA10M.xlsx'
    data = data.iter_rain_data(data.iter_rain_row(file))
    rain = rain.iter_rains(36, 1.28, data)

