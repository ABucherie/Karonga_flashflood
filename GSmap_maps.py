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
# choose event manually for saving in the right folder
i=17
# choosing the time slice 
startYear, startMonth,startDay, startHr = (2004,1,27,8)
endYear, endMonth,endDay, endHr = (2004,1,27,12)
# create a date variable for the start of the timeperiod to analyse
startDate = dt.datetime(year=startYear, month=startMonth, day=startDay, hour=startHr)
endDate = dt.datetime(year=endYear, month=endMonth, day=endDay, hour=endHr)

#read and crop the data
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20171201_20180501.nc')
#ncregion=nc.sel(lon= slice(32,36), lat=slice(-12,-8), time=startDate)
#ncregion['Gauge-calibratedRain'].plot()

#%%
#extraction of the parameter for the defined time period
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20171201_20180501.nc')           # 2017/2018 for i from 0 to 3
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20161201_20170501.nc')           # 2016/2017 for i  from 4 to 5
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20151201_20160501.nc')           # 2015/2016 for i  from 6 to 7
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20141201_20150501.nc')            # 2014/2015 for i  from 8 to 9
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20131201_20140501.nc')            # 2013/2014 for i  from 10 to 12
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20121201_20130501.nc')           # 2012/2013 for i  from 13
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20081201_20090501.nc')           # 2008/2009 for i  from 14
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20061201_20070501.nc')           # 2006/2007 for i  from 15
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20051201_20060501.nc')           # 2005/2006 for i  from 16
nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20031201_20040501.nc')           # 2005/2006 for i  from 17

nc=nc.sel(lon= slice(32,36), lat=slice(-12,-8),time=slice(startDate,endDate))
nc= nc.where(nc['Gauge-calibratedRain']!=0.)
param= nc['Gauge-calibratedRain'].sel(lon= slice(32,36), lat=slice(-12,-8),time=slice(startDate,endDate))
print(param.coords)

#%%
lon_corner=np.linspace(32,36,41)                # creating lat/lon of N+1 (=18 dimension size)
lat_corner=np.linspace(-12,-8,41)
llons,llats=np.meshgrid(lon_corner, lat_corner)        # converting lon lat of corner-pixel for the meshgrid
lon= param.coords['lon'].values                # extracting lat/lon from xarray as 1D array for the mid-pixel
lat =param.coords['lat'].values

#%%
fig = plt.figure(figsize=(10,10))  
    
for t in range(len(param)):
    print(t)
    
    m= Basemap(projection='merc',llcrnrlat=-12,urcrnrlat=-8,llcrnrlon=32,urcrnrlon=36,lat_ts=0.1,resolution='i')
    x, y = m(llons, llats)                  # converting lon lat of corner for the pixel map
    m.pcolormesh(x, y, param[t], vmin=param.min(), vmax=param.max())
          # plotting the pixel map
    m.drawcoastlines()
    m.drawcountries()
    cb=m.colorbar()
    cb.set_label(label=param.attrs['units'],fontsize=12)
    
    plt.xlabel('Longitude', fontsize=16)
    plt.ylabel('Latitude', fontsize=16)
    plt.title (str(param.attrs["standard_name"]) +' : timestep' + str(np.datetime64(param.time[t].values,'h')), fontsize=16)
    
    m.drawmapscale(35.5, -8.2, 0, 0, 100, barstyle='fancy')          # plot a scale bar
    fig.savefig('D:\Python_Scripts_Malawi\GSmap\Results\Event'+str(i)+'\GSmap'+str(np.datetime64(param.time[t].values,'h'))+'.png', dpi=300)
    plt.clf()
