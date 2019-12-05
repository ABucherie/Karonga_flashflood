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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import xarray as xr
from netCDF4 import Dataset 
import matplotlib.gridspec as gridspec 
#%%
# open parameters  dataset
nct=xr.open_dataset(r'D:\DATA_ncdf/2mtemperature.nc')
ncc=xr.open_dataset(r'D:\DATA_ncdf/cape.nc')
ncv=xr.open_dataset(r'D:\DATA_ncdf/VolSoilWater.nc')
ncwU=xr.open_dataset(r'D:\DATA_ncdf/Uwind.nc')
ncwV=xr.open_dataset(r'D:\DATA_ncdf/Vwind.nc')

# compute total Wind speed and meteorological wind direction
WM= np.sqrt(ncwU.u10**2+ncwV.v10**2)    # compute total Wind speed
WM.attrs["units"], WM.attrs["long_name"] =ncwU.u10.attrs["units"], 'Wind speed'
MWD= (180/ np.pi) * np.arctan2(-ncwU.u10,-ncwV.v10)      # compute total meteorological wind direction
MWD.attrs["units"], MWD.attrs["long_name"] ='deg', 'meteorological wind direction'

# Convert to celsius and change labels from Kelvin to Celsius
Tdeg = nct.t2m - 273.15
Tdeg.attrs = nct.t2m.attrs
Tdeg.attrs['units'] = 'deg C'

#%%
# choosing the 2 locations 
lon_loc = [34.25, 33.75]
lat_loc = [-10, -10]

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
                   ['Event16',2006,4,5,12,   2006,4,6,5]])

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
                   ['Event16',2006,4,3,12,   2006,4,10,5]])

TimePeriod= pd.DataFrame(data=tp[1:,1:], index=tp[1:,0], columns=tp[0,1:])
TimePeriod= TimePeriod.astype('int64')

print(TimePeriod)


##%% testing if loo work 
#for i in range(len(FF_list)):
#    print(i)
#    
#    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
#    endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
#    startDate = dt.datetime(year=TimePeriod.startYear[i], month=TimePeriod.startMonth[i], day=TimePeriod.startDay[i], hour=TimePeriod.startHr[i])
#    endDate = dt.datetime(year=TimePeriod.endYear[i], month=TimePeriod.endMonth[i], day=TimePeriod.endDay[i], hour=TimePeriod.endHr[i])
#    

#%%
i=14 # choose the event to evaluate
#for i in range(len(FF_list)):    # or calcutate over a loop for all events

startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
startDate = dt.datetime(year=TimePeriod.startYear[i], month=TimePeriod.startMonth[i], day=TimePeriod.startDay[i], hour=TimePeriod.startHr[i])
endDate = dt.datetime(year=TimePeriod.endYear[i], month=TimePeriod.endMonth[i], day=TimePeriod.endDay[i], hour=TimePeriod.endHr[i])

# extract temperature for the 2 locations for the given slice time
nct1 =Tdeg.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
nct2 =Tdeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))

# extract cape  for the 2 locations for the given slice time
ncc1 =ncc.cape.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
ncc2 =ncc.cape.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))

# extract volumetric soil water  for the 2 locations for the given slice time
ncv1 =ncv.swvl1.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
ncv2 =ncv.swvl1.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))

# Extract wind speed and meteorological wind direction
ncWM1=WM.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
ncWM2=WM.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate)) 
ncWD1=MWD.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
ncWD2=MWD.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))

 
#create the timestamps for FF events
EventT=Tdeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(nct1.max(), nct2.max())
EventT.attrs["units"], EventT.attrs["long_name"] =nct1.attrs["units"], nct1.attrs["long_name"]
EventC=ncc.cape.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncc1.max(), ncc2.max())
EventC.attrs["units"], EventC.attrs["long_name"] =ncc1.attrs["units"], ncc1.attrs["long_name"]
EventS=ncv.swvl1.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncv1.max(), ncv2.max())+0.05
EventS.attrs["units"], EventS.attrs["long_name"] =ncv1.attrs["units"], ncv1.attrs["long_name"]
EventWM=WM.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncWM1.max(), ncWM2.max()) +0.5
EventWM.attrs["units"], EventWM.attrs["long_name"] =ncWM1.attrs["units"], ncWM1.attrs["long_name"]
EventWD=MWD.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncWD1.max(), ncWD1.max())+ 20
EventWD.attrs["units"], EventWD.attrs["long_name"] =ncWD1.attrs["units"], ncWD1.attrs["long_name"]


# plotting a time serie at 2 X Y locations

fig = plt.figure(figsize=(13,13))

gs = gridspec.GridSpec(5,1) 
ax1=plt.subplot(gs[0,0])
ax2=plt.subplot(gs[1,0])
ax3=plt.subplot(gs[2,0])
ax4=plt.subplot(gs[3,0])
ax5=plt.subplot(gs[4,0])
gs.update(wspace=0 ,hspace=0.7) 

#axis 1 : temperature
nct1.plot(ax=ax1, color='blue', label='location Lake: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
nct2.plot(ax=ax1, color='green', label='location Land: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
EventT.plot(ax=ax1, color='red', linewidth=5)

#axis 2 : cape
ncc1.plot(ax=ax2, color='blue')
ncc2.plot(ax=ax2, color='green')
EventC.plot(ax=ax2, color='red', linewidth=5)

#axis 3 : volumetric soil water
ncv1.plot(ax=ax3, color='blue')
ncv2.plot(ax=ax3, color='green')
EventS.plot(ax=ax3, color='red', linewidth=5)

#axis 4 : Wind speed
ncWM1.plot(ax=ax4, color='blue')
ncWM2.plot(ax=ax4, color='green')
EventWM.plot(ax=ax4, color='red', linewidth=5)

#axis 5 : meteorological wind direction
ncWD1.plot(ax=ax5, color='blue')
ncWD2.plot(ax=ax5, color='green')
EventWD.plot(ax=ax5, color='red', linewidth=5)

ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\Event'+str(i)+'\graph_event'+str(i)+'_LandLake.png', dpi=300)
plt.clf()


