# Test influxdb client for v1 interface.
# This uses the python library influxdb, which works with InfluxDB v1.
# This is not the same as the python library influxdb-client,
# which is for InfluxDB v2.
# Home Assistant reports that InfluxDB is version 1.8.10.
# From https://github.com/influxdata/influxdb-python
# pip install influxdb
# pip install ciso8601
#
# This v1 client uses the simpler username/password authentication.
# The v2 client (https://pypi.org/project/influxdb-client/#queries)
# uses tokens for authentication.
#
# We connect to the InfluxDB server running on Home Assistant
# through port 8086.
# You must have a user name registered on the InfluxDB admin / Users panel.
#
# You may need to play with the Explore page on InfluxDB on HA.
# For example, SHOW TAG KEYS ON "homeassistant" FROM "°C"
# shows tagKey = domain and entity_id.
# "Measurements" are based on the units of the measurements,
# assigned by Home Assistant.  For example, '°C', 'hPa', '%'.
#
# InfluxDB uses date-times in ISO8601 format, in the UTC timezone.
# We use ciso8601 to parse, but datetime will also work if you
# remove the trailing Z.
#
# David Villeneuve
# 2023/02/08

from influxdb import InfluxDBClient
from datetime import datetime
from dateutil import tz
import ciso8601     #can parse datetime strings with trailing Z

username = 'david'
password = 'david'
dbname = 'homeassistant'

client = InfluxDBClient('homeassistant.local', 8086, 
        username, password, dbname)
print(client)

version = client.ping()     #check connection, print InfluxDB version number
print( '\nInfluxDB version {}'.format(version) )

db = client.get_list_database()     #get list of all available databases
print( '\nDatabases: {}'.format(db) )

meas = client.get_list_measurements()   #get list of all measurements
print( '\nMeasurements: {}'.format(meas) )

print( '\nMeasurement -- entity_id' )
# series = client.get_list_series( measurement='°C' ) #gives entities in this measurement
series = client.get_list_series( ) #measurement=None gives all entities
for str in series:
    items = str.split(',')
    meas = items[0] #like Lumens
    entities = items[2].split('=')  #entity_id=outdoor_temperature
    entity = entities[1]
    print( '{} -- {}'.format( meas, entity ) )


# Query a specific measuremnt for a given time period
# Make sure that the measurement name in the query, "Lumens",
# exists in your database, or change to another measurement.

dt = datetime( 2021, 7, 9, 12, 0, 0 )       #InfluxDB uses UTC timezone
dt = dt.isoformat() + 'Z'
# print( dt )
dt2 = datetime( 2021, 7, 12, 12, 0, 0 )       #InfluxDB uses UTC timezone
dt2 = dt2.isoformat() + 'Z'


# res = client.query( 'SELECT value FROM "homeassistant"."autogen"."Lumens"'
    # ' WHERE time > \'2021-07-09T12:00:00.000000000Z\'' )
res = client.query( 'SELECT value FROM "%"'
    ' WHERE time > \'{}\' AND time < \'{}\''.format(dt,dt2) )

print( '\nLength of response: {}'.format( len(res) ) )

meas = list( res.get_points( measurement='%' ) )   #filter by measurement
print( 'Length of measurement points: {}'.format( len(meas) ) )
print( 'First point: {}'.format( meas[0] ) )

value = list( range(len(meas)) )
dt = list( range(len(meas)) )
for j in range(len(meas)):  #convert ISO times to Python datetime objects
    timestr = meas[j]['time']   #time string like 2021-07-09T12:00:00.000000000Z
    dt[j] = ciso8601.parse_datetime( timestr )
    value[j] = meas[j]['value']
    
for j in range(10):
    print( dt[j], value[j] )


#####################################################
# Read a measurement that has more than one entity_id (i.e. sensor name)

# res = client.query( 'SELECT * FROM "°C" '
    # ' WHERE time > \'2023-02-09T01:00:00.000000000Z\' '
    # ' AND ("entity_id"=\'bme280_temperature\' OR '
    # ' "entity_id"=\'hallway_temperature\' OR '
    # ' "entity_id"=\'outdoor_water_temperature\' OR '
    # ' "entity_id"=\'outdoor_temperature\') '
    # )

res = client.query( 'SELECT entity_id, value FROM "°C" '
    ' WHERE time > \'2023-02-09T01:00:00Z\' '
    )

print( 'Length of response: {}'.format( len(res) ) )
#print( res )
meas = list( res.get_points( measurement='°C' ) )   #filter by measurement
print( 'Length of measurement points: {}'.format( len(meas) ) )
print( 'First point: {}'.format( meas[0] ) )

for j in range(10):
    print( meas[j]['time'], meas[j]['value'], meas[j]['entity_id'] )

