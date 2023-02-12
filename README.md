# InfluxDB_HomeAssistant
Sample Python code showing how to read values from an InfluxDB running on Home Assistant

## Home Assistant
Home Assistant is a popular open-source home automation suite that runs on small computers 
like the Raspberry Pi.
[Home Assistant](https://www.home-assistant.io/) 
runs a number of add-ons in Docker containers to extend functionality.
One such add-in is [InfluxDB](https://www.influxdata.com/).

## InfluxDB
[InfluxDB](https://www.influxdata.com/) is a well-supported database platform
that is designed to handle time-series data such as the sensor readings
produced by Home Assistant.  (This is not InfluxDB Cloud.)  By default, 
all of Home Assistant sensors (entities) will write into the database.

Note that this is not the same as the Home Assistant Recorder,
which does not keep values for very long.

InfluxDB is added to Home Assistant through Settings / Add-ons / Add-on Store 
(bottom-right), then search for Influx.  
I assume that you have configured InfluxDB correctly so that it
works with Home Assistant, and is adding data to a database
called "homeassistant".  

You also need to create a User with all permissions.  
In my case, my username is david.

Home Assistant communicates with InfluxDB via an API
that is reached through port 8086 on the local host, http://127.0.0.1.

An external program can do the same, using the IP address
of the computer on which the Home Assistant is running.
This might be an IP address like 192.168.1.101.
Or it might be reached by mDNS like homeassistant.local.
A standard browser should be able to see the Home Assistant
web interface at homeassistant.local:8123.
The InfluxDB API is reached at homeassistant.local:8086,
but it does not have a web interface.

## Python access to InfluxDB on Home Assistant

There are two versions of InfluxDB: 1 and 2.  
Home Assistant is using version 1.8.10 as of February 2023.
The Python client for this version is influxdb 5.3.1
[influxdb](https://pypi.org/project/influxdb/).
There is a different Python client for InfluxDB v2, influxdb-client.
Do not use that one.

## Install influxdb client

Using a standard Python distribution like Anaconda:
```
pip install influxdb
pip install ciso8601 (optional)
```
## Run the test program

You will have to edit testv1.py first to enter your InfluxDB
username and password (from david).
You may have to change the IP address of the Home Assistant computer.

```
python testv1.py  (on Windows)
python3 testv1.py (on Linux)
```

This should connect with the InfluxDB program on your Home Assistant computer.
It will print the version number of the InfluxDB server,
and the names of the databases.
It will print the "measurements", which in Home Assistant are the units
of the measurement, e.g. % or GB or hPa.
It will then print the Home Assistant entity_id connected with each measurement.
I have over 300 such entities.
It will then run a couple of database queries and print some times
and values.  These queries may not work on your setup if you
do not have similar measurements.

Note that InfluxDB stores times using the UTC timezone (Greenwich).
The returned dates will be in this time zone.

The top of the output should looke something like this:
```
<influxdb.client.InfluxDBClient object at 0x000002815DDC8400>

InfluxDB version 1.8.10

Databases: [{'name': '_internal'}, {'name': 'Weather_outside'}, {'name': 'homeassistant'}]

Measurements: [{'name': '%'}, {'name': 'AQI'}, {'name': 'GB'}, {'name': 'GiB'}, {'name': 'Lumens'}, {'name': 'Lux'}, {'name': 'MHz'}, {'name': 'Mbps'}, {'name': 'MiB'}, {'name': 'Minutes'}, {'name': 'Pascals'}, {'name': 'UV index'}, {'name': 'W'}, {'name': 'connection(s)'}, {'name': 'dBm'}, {'name': 'degrees'}, {'name': 'hPa'}, {'name': 'kPa'}, {'name': 'km'}, {'name': 'km/h'}, {'name': 'lux'}, {'name': 'lx'}, {'name': 'mm'}, {'name': 'notifications'}, {'name': 'pending update(s)'}, {'name': 'state'}, {'name': 'steps'}, {'name': 'ug/m3'}, {'name': '°'}, {'name': '°C'}]

Measurement -- entity_id
% -- hallway_light_intensity
% -- aeotec_limited_zwa005_trisensor_battery_level
% -- aht10_humidity
% -- bme280_humidity
% -- cold_air_return_humidity
% -- disk_use_percent
%
```

## Save the InfluxDB data to a local file

You can analyse the InfluxDB data on Home Assistant using
the built-in queries.
However it might be preferable to pull all the data off of
Home Assistant so that you can analyse on a larger computer
using Python.  Also, the InfluxDB database gets quite large
after running for a few years, causing backup files to be large.

A sample program, InfluxDB2File.py, is provided to show how
all of the values of an entity_id are read into a numpy file.
You will need to change the username and password,
and probably some entries in entity.

Here, a list of pairs of measurements (e.g. %) and entity_ids
(e.g. outdoor_temperature) are entered in the variable `entity`.
The date-times and readings are written into the numpy-format file
for each entity_id.  TDate-times are written in POSIX format,
i.e. floating point numbers with the number of seconds
after 1 January 1970.  Again, UTC timezone is used.

```
python InfluxDB2File.py
```

## Reading the local files

The sample program PlotInfluxDBdata.py will read one of the numpy files
and plot the time series using matplotlib.  All times are in UTC.
Again, you will have to edit the code to point to one of your files.

```
python PlotInfluxDBdata.py
```