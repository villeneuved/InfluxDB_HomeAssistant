# Read numpy file that was created from Home Assistant InfluxDB.
# Created by InfluxDB2File.py.

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as md

base_folder = '../Data_To_20230210/'
filename = 'sunroom_temperature_probe_2.npy'
d = np.load( base_folder + filename )     #(npts,2)
sz = d.shape
npts = sz[0]

dt = [x for x in range(npts)]
y = [x for x in range(npts)]

for j in range(npts):
    dt[j] = datetime.fromtimestamp( d[j,0], timezone.utc )
    y[j] = d[j,1]
    
print( 'File {} has dates from {} to {}'.format( filename, dt[0], dt[-1] ) )

fig,ax = plt.subplots()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M')
ax.plot( dt, y )
fig.autofmt_xdate(bottom=0.2, rotation=20)
plt.title( filename )
plt.xlabel( 'Date-time in UTC' )
plt.show()