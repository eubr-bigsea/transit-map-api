# transit-map-api

Python API to generate data to [transit-map](https://github.com/vasile/transit-map) application. I tried to use PHP API provided but I don't know PHP and it seems to be broken.

## Dependencies
- Python >= 2.6 ( >=3.0 may work)
- Flask (pip install flask)
- Flask-cors

## Running
``` bash
# python app.py
```
You have to follow transit-map documentation to convert GTFS data into a sqlite3 database and generate 2 files with stops and shapes. 
