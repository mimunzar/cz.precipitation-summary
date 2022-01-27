Precipitation Summary Tool
==========================

The tools allows to make statistics of selected rains from recorded  rain  data.
The input of the tool is data recorded in Excell sheets.  The outputs are Excell
sheets with rain statistics.


Installation
------------

To install the tool navigate to the project's folder  and  issue  the  following
command:

    conda env create -f environment.yml

Note: The program was developed with Python 3.9


Usage
-----

To make statistics from input files located in I_FOLDER issue the following
command:

    python -m src.precipitation_summary.make_summary \
        -i <I_FOLDER> \
        -o <O_FOLDER>

The program writes the statistic files to O_FOLDER.


Possible Improvements
---------------------

    - Support additional statistics
    - Support configuration of data locations in input sheets
    - Support parallel processing


Implementation TODO:
-------------------
    - Use date computation from rain module in data module
    - Remove data.write_sheet_data

