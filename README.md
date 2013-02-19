data_cleaning
=============

Miscellaneous scripts to clean data


------------------
convert_to_csv.vba
------------------

An Excel/VBA macro that converts Excel workbooks with multiple worksheets
into csv files.


-----------------
list_all_files.py
-----------------

A Python script that prints paths to files in all subfolders.
It works on both Linux and Windows.


--------------
merege_csvs.py
--------------

A Python script that merges csv files into a single file.
The csv files must have headers as their first line.


-----------------
scan_fred_data.py
-----------------

A Python script that analyzes each file in each subdirectory in a 
FRED II database dump and reports as a csv the following information:

    path,title,series,source,release,sadj,freq,units,dates,updated
