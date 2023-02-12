# Read Home Assistant InfluxDB database content to numpy files.
#
# This uses the python library influxdb, which works with InfluxDB v1.
# This is not the same as the python library influxdb-client,
# which is for InfluxDB v2.
# Home Assistant reports that InfluxDB is version 1.8.10.
# From https://github.com/influxdata/influxdb-python
# pip install influxdb
#
# This v1 client uses the simpler username/password authentication.
# The v2 client (https://pypi.org/project/influxdb-client/#queries)
# uses tokens for authentication.
#
# We connect to the InfluxDB server running on Home Assistant
# through port 8086.
# You must have a user name registered on the InfluxDB admin / Users panel.
#
# InfluxDB uses date-times in ISO8601 format, in the UTC timezone.
# We use ciso8601 to parse, but datetime will also work if you
# remove the trailing Z.
#
# David Villeneuve
# 2023/02/08

from influxdb import InfluxDBClient
from datetime import datetime, timezone
import ciso8601     #can parse datetime strings with trailing Z
import numpy as np

entities = [
        '°C', 'bme280_temperature', 
        '°C', 'cold_air_return_temperature', 
        '°C', 'gatineau_temperature', 
        '°C', 'hallway_temperature', 
        '°C', 'hot_air_supply_temperature', 
        '°C', 'outdoor_temperature', 
        '°C', 'outdoor_water_temperature', 
        '°C', 'sunroom_temperature', 
        '°C', 'sunroom_temperature_probe', 
        '°C', 'sunroom_temperature_probe_2', 
        '%', 'cold_air_return_humidity', 
        '%', 'gatineau_humidity', 
        '%', 'hallway_humidity', 
        '%', 'hot_air_supply_humidity', 
        '%', 'outdoor_humidity', 
        '%', 'sunroom_humidity', 
        'hPa', 'cold_air_return_pressure', 
        'hPa', 'hallway_pressure_hpa', 
        'hPa', 'hot_air_supply_pressure', 
        'hPa', 'outdoor_pressure_hpa', 
        'mm', 'outdoor_rainfall', 
        'Lux', 'outdoor_light'
        ]

# FUnction to read measurements, save to file

def save_entity( entity, measurement="°C" ):

    res = client.query( 
        'SELECT entity_id, value FROM "{}" '
        ' WHERE "entity_id"=\'{}\' '.format( measurement, entity )
        )

    # Check that we can convert the UTC time string to POSIX timestamp
    # (float of seconds since 1 Jan 1970).
    # Our times are in UTC, dt2 is in UTC.
    # timestamp = dt.timestamp()
    # print(timestamp)
    # dt2 = datetime.fromtimestamp(timestamp, timezone.utc)
    # print( dt2 )

    meas = list( res.get_points( ) )   #filter by measurement
    tv = np.empty( (len(meas),2) )

    for j in range(len(meas)):
        dt = ciso8601.parse_datetime( meas[j]['time'] ) #convert time to datetime
        timestamp = dt.timestamp()      #convert datetime to POSIX timestamp
        tv[j,0] = timestamp
        tv[j,1] = meas[j]['value']
        # print( meas[j]['time'], meas[j]['value'], meas[j]['entity_id'] )

    np.save( entity, tv )
    
    
username = 'david'
password = 'david'
dbname = 'homeassistant'

client = InfluxDBClient('homeassistant.local', 8086, 
        username, password, dbname)
print(client)

version = client.ping()     #check connection, print InfluxDB version number
print( 'InfluxDB version {}'.format(version) )

k = 0
for j in range(int(len(entities)/2)):
    print( 'Saving {}'.format( entities[k+1] ) )
    save_entity( entities[k+1], entities[k] )
    k += 2


