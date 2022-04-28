#!/bin/bash -l

CONDA_ENV=$1
shift
PROG_ARGS=$@

conda activate ${CONDA_ENV} || exit 1
python -um src.precipitation_summary.make_summary ${PROG_ARGS} || exit 1

