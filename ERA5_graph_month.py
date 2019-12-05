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
MWD= (180/ np.pi) * np.arctan2(-ncwU.u10,-ncwV.v10)      # compute total meteorological wind direction from -180 to 180
#MWD= 180+ (180/ np.pi) * np.arctan2(ncwU.u10,ncwV.v10)      # compute total meteorological wind direction from 0 to 360
MWD.attrs["units"], MWD.attrs["long_name"] ='deg', 'meteorological wind direction'

# Convert to celsius and change labels from Kelvin to Celsius
Tdeg = nct.t2m - 273.15
Tdeg.attrs = nct.t2m.attrs
Tdeg.attrs['units'] = 'deg C'

#%%
# choosing the 2 locations 
lon_loc = [33.75, 34.00]
lat_loc = [-9.75, -10.25]

#%%
startYear, startMonth,startDay, startHr = (2009,3,1,1)
endYear, endMonth,endDay, endHr = (2009,3,31,23)
# create a date variable for the start of the timeperiod to analyse
startDate = dt.datetime(year=startYear, month=startMonth, day=startDay, hour=startHr)
endDate = dt.datetime(year=endYear, month=endMonth, day=endDay, hour=endHr)
#for i in range(len(FF_list)):    # or calcutate over a loop for all events
#%%

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
#MWD=MWD.resample(time='1D').mean(dim='time')

ncWM1=WM.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
ncWM2=WM.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate)) 
ncWD1=MWD.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
ncWD2=MWD.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))

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
nct1.plot(ax=ax1, color='blue', label='location A: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
nct2.plot(ax=ax1, color='green', label='location B: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))

#axis 2 : cape
ncc1.plot(ax=ax2, color='blue')
ncc2.plot(ax=ax2, color='green')

#axis 3 : volumetric soil water
ncv1.plot(ax=ax3, color='blue')
ncv2.plot(ax=ax3, color='green')

#axis 4 : Wind speed
ncWM1.plot(ax=ax4, color='blue')
ncWM2.plot(ax=ax4, color='green')

#axis 5 : meteorological wind direction
ncWD1.plot(ax=ax5, color='blue')
ncWD2.plot(ax=ax5, color='green')


ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')
ax5.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\ERA5_JanFeb2018_graph.png', dpi=300)
plt.clf()


