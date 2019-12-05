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

#33.75990,-9.67276
#33.75394,-9.75211
#33.75201,-9.84438
#33.84720,-9.85051
#33.85523,-10.06259
#33.84907,-10.15964
#33.94967,-10.15724
#33.94619,-10.24527
#33.95561,-10.35287

#definition of the FF events
Events = np.array([['','startYear','startMonth','startDay', 'startHr','endYear','endMonth','endDay', 'endHr' ],
                   ['Event0',2018,4,10,22,   2018,4,13,12], 
                   ['Event1',2018,1,30,22,   2018,1,31,12], 
                   ['Event2',2018,1,21,18,   2018,1,23,8],
                   ['Event3',2018,1,12,18,   2018,1,13,15], 
                   ['Event4',2017,4,1,0,     2017,4,2,12 ],
                   ['Event5',2017,1,6,14,    2017,1,7,6],
                   ['Event6',2016,2,28,0,    2016,3,1,0],
                   ['Event7',2016,1,31,12,   2016,2,1,12], 
                   ['Event8',2015,1,18,18,   2015,1,19,12],
                   ['Event9',2015,1,2,12,    2015,1,3,12 ],
                   ['Event10',2014,3,19,12,  2014,3,21,12 ],
                   ['Event11',2014,2,24,12,  2014,2,25,23],
                   ['Event12',2014,1,29,12,  2014,1,30,12],
                   ['Event13',2013,3,26,12,  2013,3,27,5],
                   ['Event14',2009,3,8,12,   2009,3,9,5],
                   ['Event15',2007,1,22,12,  2007,1,23,5],
                   ['Event16',2006,4,5,12,   2006,4,6,5],
                   ['Event17',2004,1,27,12,  2004,1,28,1]])

FF_list= pd.DataFrame(data=Events[1:,1:], index=Events[1:,0], columns=Events[0,1:])
FF_list= FF_list.astype('int64')
#definition of the time period to analyse in the graph
tp = np.array([['','startYear','startMonth','startDay', 'startHr','endYear','endMonth','endDay', 'endHr' ],
                   ['Event0',2018,4,9,0,    2018,4,16,23], 
                   ['Event1',2018,1,28,0,   2018,2,1,23], 
                   ['Event2',2018,1,21,0,   2018,1,23,23],
                   ['Event3',2018,1,12,0,   2018,1,14,0], 
                   ['Event4',2017,3,27,0,   2017,4,6,0 ],
                   ['Event5',2017,1,3,0,    2017,1,11,23],
                   ['Event6',2016,2,20,0,   2016,3,8,23],
                   ['Event7',2016,1,29,0,   2016,2,4,23], 
                   ['Event8',2015,1,14,0,   2015,1,22,0],
                   ['Event9',2014,12,28,0,  2015,1,6,0 ],
                   ['Event10',2014,3,17,12, 2014,3,26,12],
                   ['Event11',2014,2,20,12, 2014,2,28,23],
                   ['Event12',2014,1,25,12,  2014,2,1,23],
                   ['Event13',2013,3,23,12,  2013,3,29,12],
                   ['Event14',2009,3,4,12,   2009,3,13,5],
                   ['Event15',2007,1,18,12,  2007,1,27,5],
                   ['Event16',2006,4,3,12,   2006,4,10,5],
                   ['Event17',2004,1,25,12,  2004,1,31,5]])

TimePeriod= pd.DataFrame(data=tp[1:,1:], index=tp[1:,0], columns=tp[0,1:])
TimePeriod= TimePeriod.astype('int64')

#%%
i=17  # choose the event to evaluate
startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
startDate = dt.datetime(year=TimePeriod.startYear[i], month=TimePeriod.startMonth[i], day=TimePeriod.startDay[i], hour=TimePeriod.startHr[i])
endDate = dt.datetime(year=TimePeriod.endYear[i], month=TimePeriod.endMonth[i], day=TimePeriod.endDay[i], hour=TimePeriod.endHr[i])
#%%
# nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20171201_20180501.nc')         # for i from 0 to 3
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20161201_20170501.nc')          # for i  from 4 to 5
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20151201_20160501.nc')          # for i  from 6 to 7
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20141201_20150501.nc')           # for i  from 8 to 9
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20131201_20140501.nc')           # 2013/2014 for i  from 10
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20121201_20130501.nc')           # 2013/2014 for i  from 13
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20081201_20090501.nc')           # 2008/2009 for i  from 14
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20061201_20070501.nc')           # 2006/2007 for i  from 15
#nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20051201_20060501.nc')           # 2005/2006 for i  from 16
nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSMaP_20031201_20040501.nc')           # 2005/2006 for i  from 17

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
#create the timestamps for FF events
MAX= [ncloc0.max(), ncloc1.max(),ncloc2.max(),ncloc3.max(),ncloc4.max(),ncloc5.max(),ncloc6.max(),ncloc7.max(),ncloc8.max()]
#Event=ncloc0.sel(time=slice(startevent,endevent))*0 + max(ncloc0.max(),ncloc1.max())
Event=ncloc0.sel(time=slice(startevent,endevent))*0 + max(MAX)+2
Event.attrs["units"], Event.attrs["long_name"] =ncloc0.attrs["units"], ncloc0.attrs["long_name"]

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
Event.plot(ax=ax1, color='red', linewidth=5)

##axis 2 : location 2 and 3 (kasisi, kasoba, Nkhomi)
ncloc2.plot(ax=ax2,color='darkblue', label='Kasisi')
ncloc3.plot(ax=ax2,color='green', label='Kasoba/Nkhomi')
Event.plot(ax=ax2, color='red', linewidth=5)

##axis 3 : location 4,5 and 6 (Lwasho, bwaye, kasimba)
ncloc4.plot(ax=ax3, color='cyan',label='Lwasho')
ncloc5.plot(ax=ax3, color='darkgreen', label='Bwaye')
ncloc6.plot(ax=ax3, color='purple', label='Kasimba')
Event.plot(ax=ax3, color='red', linewidth=5)

##axis 4 : location 7,8  (Remero, sabi)
ncloc7.plot(ax=ax4, color='blue',label='Remero')
ncloc8.plot(ax=ax4, color='lightgreen', label='Sabi')
Event.plot(ax=ax4, color='red', linewidth=5)

ax1.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax2.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax3.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax4.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\GSmap\Results\Event'+str(i)+'\graph_event'+str(i)+'_9loc.png', dpi=300)
#plt.clf()


