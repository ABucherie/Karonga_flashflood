# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 16:21:46 2017

@author: Agathe Bucherie
"""

'''
The script is to read NCDF file of GSmap and create movies of maps for different hours corresponding to Flash flood events

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
nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSmap_crop_merged.nc')           # crop and concatenated GSmap file

#test with one event - no basemap.
i=17
startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
param= nc['Gauge-calibratedRain'].sel(time=slice(startevent,endevent))
cumrain_17= param.sum(dim='time')
cumrain_17.plot()

#%%
lon_corner=np.linspace(32,36,41)                        # creating lat/lon of N+1 (=18 dimension size)
lat_corner=np.linspace(-12,-8,41)
llons,llats=np.meshgrid(lon_corner, lat_corner)        # converting lon lat of corner-pixel for the meshgrid
lon= nc.coords['lon'].values                        # extracting lat/lon from xarray as 1D array for the mid-pixel
lat =nc.coords['lat'].values

fig = plt.figure(figsize=(10,10))  
    
for i in range(len(FF_list)):    # or calcutate over a loop for all events
    print(i)
    
    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
    endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
    
    cumrain= nc['Gauge-calibratedRain'].sel(time=slice(startevent,endevent))
    cumrain= cumrain.sum(dim='time')
    cumrain= cumrain.where(cumrain!=0.)
    
    m= Basemap(projection='merc',llcrnrlat=-12,urcrnrlat=-8,llcrnrlon=32,urcrnrlon=36,lat_ts=0.1,resolution='i')
    x, y = m(llons, llats)                  # converting lon lat of corner for the pixel map
    m.pcolormesh(x, y, cumrain, vmin=cumrain.min(), vmax=cumrain.max())
    m.drawcoastlines()
    m.drawcountries()
    cb=m.colorbar()
    cb.set_label(label='mm in '+ str(np.datetime64((endevent),'h')-np.datetime64((startevent),'h')),fontsize=14)
    
    plt.xlabel('Longitude', fontsize=16)
    plt.ylabel('Latitude', fontsize=16)
    plt.title (' Cumulative precipitation (mm) over the '+ str(np.datetime64((endevent),'h')-np.datetime64((startevent),'h'))+' duration event \n Event '+ str(i) +' : ' + str(np.datetime64(startevent,'h')) + ' to '+ str(np.datetime64(endevent,'h')), fontsize=16)
    
    m.drawmapscale(35.5, -8.2, 0, 0, 100, barstyle='fancy')          # plot a scale bar
    
    fig.savefig('D:\Python_Scripts_Malawi\GSmap\Results\CumRain_events\CumRain_event'+str(i)+'.png', dpi=300)
    plt.clf()
