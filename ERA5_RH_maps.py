# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 16:21:46 2017

@author: Agathe Bucherie
"""

'''
The script is a test to try to read NCDF file and to plot timeline and maps

'''
#%%
import datetime as dt   # Python standard library datetime  module
from datetime import timedelta, date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import xarray as xr
from netCDF4 import Dataset

#%%
ncRH=xr.open_dataset(r'D:\DATA_ncdf/ERA5_RH500_850.nc')

#%% 
#definition of the FF events corresponding to the entire GSmap rainfall event (updated)
Events = np.array([['','startYear','startMonth','startDay', 'startHr','endYear','endMonth','endDay', 'endHr' ],
                   ['Event0',2018,4,10,18,   2018,4,11,2], 
                   ['Event1',2018,1,30,19,   2018,1,31,6], 
                   ['Event2',2018,1,22,15,   2018,1,23,5],
                   ['Event3',2018,1,12,16,   2018,1,13,7], 
                   ['Event4',2017,4,1,19,    2017,4,2,4],
                   ['Event5',2017,1,6,19,    2017,1,6,23],
                   ['Event6',2016,2,28,16,   2016,2,29,0],
                   ['Event7',2016,1,31,14,   2016,2,1,7], 
                   ['Event8',2015,1,18,22,   2015,1,19,11],
                   ['Event9',2015,1,3,2,     2015,1,3,7],
                   ['Event10',2014,3,19,19,  2014,3,20,3],
                   ['Event11',2014,2,24,17,  2014,2,24,23],
                   ['Event12',2014,1,30,14,  2014,1,30,17],
                   ['Event13',2013,3,26,14,  2013,3,27,0],
                   ['Event14',2009,3,8,23,   2009,3,9,4],
                   ['Event15',2007,1,22,18,  2007,1,23,3],
                   ['Event16',2006,4,5,17,   2006,4,6,4],
                   ['Event17',2004,1,27,11,  2004,1,27,14]])

FF_list= pd.DataFrame(data=Events[1:,1:], index=Events[1:,0], columns=Events[0,1:])
FF_list= FF_list.astype('int64')


#%% 
# choosing i the FF event reference for saving
i=15
startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])

startDate=startevent-timedelta(hours=3)
endDate= endevent

# extraction of the parameter for the defined time period
rhmap=ncRH.r.sel(time=slice(startDate,endDate))
rhmap.attrs["units"], rhmap.attrs["long_name"] =ncRH.attrs["units"], ncRH.attrs["long_name"]

'''
compute  parameter : RH
'''
param=rhmap    # nccmap : for cape

fig = plt.figure(figsize=(10,10))  

lon_corner=np.linspace(31.875,36.125,18)                # creating lat/lon of N+1 (=18 dimension size)
lat_corner=np.linspace(-7.875,-12.125,18)
llons,llats=np.meshgrid(lon_corner, lat_corner)        # converting lon lat of corner-pixel for the meshgrid
lon= param.coords['longitude'].values                # extracting lat/lon from xarray as 1D array for the mid-pixel
lat =param.coords['latitude'].values

fig = plt.figure(figsize=(10,10))  
    
for t in range(len(param)):
    print(t)
    
    m= Basemap(projection='merc',llcrnrlat=-12.125,urcrnrlat=-7.875,llcrnrlon=31.875,urcrnrlon=36.125,lat_ts=0.1,resolution='i')
    x, y = m(llons, llats)                                                                       # converting lon lat of corner for the pixel map
    m.pcolormesh(x, y, param[t], vmin=param.quantile(0.05), vmax=param.quantile(0.95))          # plotting the pixel map
    m.drawcoastlines()
    m.drawcountries()
    cb=m.colorbar()
    cb.set_label(label=param.attrs['units'],fontsize=12)
    
    plt.xlabel('Longitude', fontsize=16)
    plt.ylabel('Latitude', fontsize=16)
    plt.title (str(param.attrs["long_name"]) +' : timestep' + str(np.datetime64(param.time[t].values,'h')), fontsize=16)
    
    m.drawmapscale(35.5, -8.2, 0, 0, 100, barstyle='fancy')          # plot a scale bar
    fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\Event'+str(i)+'\Event'+str(i)+str(param.name) +str(np.datetime64(param.time[t].values,'h'))+'.png', dpi=300)
    plt.clf()

    

