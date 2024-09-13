Precipitation Summary Tool
==========================

The tools allows to make statistics of selected rains from recorded  rain  data.
The input of the tool is data recorded in Excell sheets.  The outputs are Excell
sheets with rain statistics.


Installation
------------

To install the tool navigate to the project's folder  and  issue  the  following
command:

    docker build . -t rain_stats

The command builds a container with a name "rain_stats".


Usage
-----

To run the program, mount a folder containing an input data into  the  container
and provide the path to the folder in the container.  This can be done with  the
following command:

    docker run -v $(pwd)/data:/mnt -t rain_stats /mnt/data

Where "$(pwd)/data:/mnt" is an example of a folder containing input  data.   The
folder is mounted into the container's "/mnt".  Results  are  written  into  the
same folder to files with "stat.xlsx" suffix.


Possible Improvements
---------------------

    - Support additional statistics
    - Support parallel processing

