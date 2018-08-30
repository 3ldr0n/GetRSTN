# GetRSTN
Download RSTN's data from noaa's site. 

## Installation

```bash
pip install getrstn
```

## How to use it

```python
from getrstn import GetRSTN

day = 9
month = 4
year = 2002
path_to_files = "data/"
station = "San vito"

rstn = GetRSTN(day, month, year, path_to_files, station)

# Downloads and decompress the file.
rstn.decompress_file(download=True)

# Plots the data.
ax = rstn.plot()
```

## Compatibility
The library was tested with Python 3.6.5, and Python 2.7.14. It'll probably work with other python3 version, but i don't know if it'll work with Python 2.6 or older versions.
