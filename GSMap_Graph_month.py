# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 11:18:48 2019

@author: abu001
"""


'''
The script is done to read NCDF file  from GSmap, merge them and extract only NorthMalawi data.
Then analysis will follow with plots of timeline and maps

'''
#%%
import datetime as dt   # Python standard library datetime  module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import xarray as xr
from netCDF4 import Dataset
import scipy.special  as sp
import matplotlib.gridspec as gridspec 

#%%
# choosing the 9 locations 
lon_loc = [33.75990, 33.75394,   33.75201,  33.84720,   33.85523,   33.84907,   33.94967,    33.94619,   33.95561]
lat_loc = [-9.67276, -9.7521,   -9.84438,   -9.85051,   -10.06259,  -10.15964,  -10.15724,  -10.24527,  -10.35287]

#0,1, iponga and kyungu
#2,3 are kasisi, kasoba, Nkhomi
#4,5,6  Lwasho, bwaye, kasimba
#7,8 Remero, Sabi

startYear, startMonth,startDay, startHr = (2009,3,1,0)
endYear, endMonth,endDay, endHr = (2009,3,31,23)
# create a date variable for the start of the timeperiod to analyse
startDate = dt.datetime(year=startYear, month=startMonth, day=startDay, hour=startHr)
endDate = dt.datetime(year=endYear, month=endMonth, day=endDay, hour=endHr)

#%%
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20171201_20180501.nc')           # 2017/2018  for i from 0 to 3
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20161201_20170501.nc')           # 2016/2017  for i  from 4 to 5
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20151201_20160501.nc')           # 2015/216 for i  from 6
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20141201_20150501.nc')           # 2014/2015 for i  from 8
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20131201_20140501.nc')           # 2014/2015 for i  from 10
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20121201_20130501.nc')           # 2013/2014 for i  from 13
nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20081201_20090501.nc')           # 2008/2009 for i  from 14

nctime=nc.sel(time=slice(startDate,endDate))

ncloc0=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[0],lat=lat_loc[0], method= 'nearest')
ncloc1=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[1],lat=lat_loc[1], method= 'nearest')
ncloc2=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[2],lat=lat_loc[2], method= 'nearest')
ncloc3=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[3],lat=lat_loc[3], method= 'nearest')
ncloc4=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[4],lat=lat_loc[4], method= 'nearest')
ncloc5=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[5],lat=lat_loc[5], method= 'nearest')
ncloc6=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[6],lat=lat_loc[6], method= 'nearest')
ncloc7=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[7],lat=lat_loc[7], method= 'nearest')
ncloc8=nctime['Gauge-calibratedRain'].sel(lon=lon_loc[8],lat=lat_loc[8], method= 'nearest')


#%%
# plotting the rainfall time serie at the 9 XY locations
fig = plt.figure(figsize=(13,13))

gs = gridspec.GridSpec(4,1) 
ax1=plt.subplot(gs[0,0])
ax2=plt.subplot(gs[1,0])
ax3=plt.subplot(gs[2,0])
ax4=plt.subplot(gs[3,0])
gs.update(wspace=0 ,hspace=0.7) 

#axis 1 : location 0 and 1 (Iponga and Kyungu, kasantha and kibwe)
ncloc0.plot(ax=ax1, color='blue', label='Iponga/kyungu')
ncloc1.plot(ax=ax1, color='orange',label='Kyungu/kasantha/Kibwe')

##axis 2 : location 2 and 3 (kasisi, kasoba, Nkhomi)
ncloc2.plot(ax=ax2,color='darkblue', label='Kasisi')
ncloc3.plot(ax=ax2,color='green', label='Kasoba/Nkhomi')

##axis 3 : location 4,5 and 6 (Lwasho, bwaye, kasimba)
ncloc4.plot(ax=ax3, color='cyan',label='Lwasho')
ncloc5.plot(ax=ax3, color='darkgreen', label='Bwaye')
ncloc6.plot(ax=ax3, color='purple', label='Kasimba')

##axis 4 : location 7,8  (Remero, sabi)
ncloc7.plot(ax=ax4, color='blue',label='Remero')
ncloc8.plot(ax=ax4, color='lightgreen', label='Sabi')

ax1.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax2.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax3.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax4.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\GSmap\Results\graph_march2009.png', dpi=300)
#plt.clf()


