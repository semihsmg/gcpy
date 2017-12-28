gcpy
===================================
This app keeps record of date and time. Calculates time difference between two records and sums the times of days, displays and export to txt file.

Pre-requisites
--------------

- Python 3.x

Getting Started
---------------

You can edit the destination for the files with changing destination variable in the calculations.py
If you do not, application creates a folder to this destination as \gcpy\{month}_{year} then creates {month}_{year}.db in it.

Files
---------------

- master.py: Access to all functions in the app
- record_time.py: Record date and time of that moment
- calc_time.py: Calculates time differences between first and last record. Then exports a txt file named as {month} _ {year}.txt 
