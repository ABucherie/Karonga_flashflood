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
import plotly.plotly as py
import plotly.graph_objs as go


#%%
# open parameters  dataset
nct=xr.open_dataset(r'D:\DATA_ncdf/2mtemperature.nc')
ncc=xr.open_dataset(r'D:\DATA_ncdf/cape.nc')
ncv=xr.open_dataset(r'D:\DATA_ncdf/VolSoilWater.nc')
ncwU=xr.open_dataset(r'D:\DATA_ncdf/Uwind.nc')
ncwV=xr.open_dataset(r'D:\DATA_ncdf/Vwind.nc')

#%% 
# choosing the 2 locations of lake and land
lon_loc = [34.25, 33.75]
lat_loc = [-10, -10]


#%% Computing the diurnal variation of cape in January and comparing with April in a location in the land and over the lake
nccJan= ncc.where(ncc['time.month']==1)
#nccJan = nccJan.where(nccJan['cape']!=0)
CdiurJan= nccJan.cape.groupby('time.hour').mean('time')
nccApr= ncc.where(ncc['time.month']==4)
#nccApr = nccApr.where(nccApr['cape']!=0)
CdiurApr= nccApr.cape.groupby('time.hour').mean('time')

CdiurJan0 =CdiurJan.sel(longitude=lon_loc[0],latitude=lat_loc[0])   
CdiurJan1 =CdiurJan.sel(longitude=lon_loc[1],latitude=lat_loc[1])  
CdiurApr0 =CdiurApr.sel(longitude=lon_loc[0],latitude=lat_loc[0])   
CdiurApr1 =CdiurApr.sel(longitude=lon_loc[1],latitude=lat_loc[1]) 

fig = plt.figure(figsize=(8,6))
gs = gridspec.GridSpec(2,1) 
ax1=plt.subplot(gs[0,0])
ax2=plt.subplot(gs[1,0])
gs.update(wspace=0 ,hspace=0.7) 

#axis 1 : location 0 and 1 (Iponga and Kyungu, kasantha and kibwe)
CdiurJan0.plot(ax=ax1, color='blue', label='Lake')
CdiurJan1.plot(ax=ax1, color='green',label='Land')

##axis 2 : location 2 and 3 (kasisi, kasoba, Nkhomi)
CdiurApr0.plot(ax=ax2,color='blue', label='Lake')
CdiurApr1.plot(ax=ax2,color='green', label='Land')

ax1.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax2.legend(loc='top right', ncol=1, fancybox=True, shadow=True)

ax1.set_title('diurnal variation of Cape in January')
ax2.set_title('diurnal variation of Cape in April')


fig.savefig('D:\Python_Scripts_Malawi\GSmap\Results\diurnalCape.png', dpi=300)
#plt.clf()

#%% Computing the diurnal variation of cape in January and comparing with April in a location in the land and over the lake
# compute total Wind speed and meteorological wind direction

ncUJan= ncwU.where(ncwU['time.month']==1)
UdiurJan= ncUJan.u10.groupby('time.hour').mean('time')
ncVJan= ncwV.where(ncwV['time.month']==1)
VdiurJan= ncVJan.v10.groupby('time.hour').mean('time')

ncUApr= ncwU.where(ncwU['time.month']==4)
UdiurApr= ncUApr.u10.groupby('time.hour').mean('time')
ncVApr= ncwV.where(ncwV['time.month']==4)
VdiurApr= ncVApr.v10.groupby('time.hour').mean('time')

#WMJan =np.sqrt(UdiurJan**2+VdiurJan**2)
#WMApr =np.sqrt(UdiurApr**2+VdiurApr**2)
#WMJan.attrs["units"], WMJan.attrs["long_name"] ='m/s', 'Wind speed'
#WMApr.attrs["units"], WMApr.attrs["long_name"] ='m/s', 'Wind speed'
#
#WMdiurJan0 =WMJan.sel(longitude=lon_loc[0],latitude=lat_loc[0])   
#WMdiurJan1 =WMApr.sel(longitude=lon_loc[1],latitude=lat_loc[1])  
#WMdiurApr0 =WMApr.sel(longitude=lon_loc[0],latitude=lat_loc[0])   
#WMdiurApr1 =WMApr.sel(longitude=lon_loc[1],latitude=lat_loc[1]) 

MWDJan= (180/ np.pi) * np.arctan2(-UdiurJan,-VdiurJan)
MWDApr= (180/ np.pi) * np.arctan2(-UdiurApr,-VdiurApr)

MWDJan.attrs["units"], MWDJan.attrs["long_name"] ='deg', 'meteorological wind direction'
MWDApr.attrs["units"], MWDApr.attrs["long_name"] ='deg', 'meteorological wind direction'

MWDdiurJan0 =MWDJan.sel(longitude=lon_loc[0],latitude=lat_loc[0])   
MWDdiurJan1 =MWDJan.sel(longitude=lon_loc[1],latitude=lat_loc[1])  
MWDdiurApr0 =MWDApr.sel(longitude=lon_loc[0],latitude=lat_loc[0])   
MWDdiurApr1 =MWDApr.sel(longitude=lon_loc[1],latitude=lat_loc[1]) 

#plotting diurnal wind direction in the lake and land  in january and April

fig = plt.figure(figsize=(8,6))
gs = gridspec.GridSpec(2,1) 
ax1=plt.subplot(gs[0,0])
ax2=plt.subplot(gs[1,0])
gs.update(wspace=0 ,hspace=0.7) 

#axis 1 : january 
MWDdiurJan0 .plot(ax=ax1, color='blue', label='Lake')
MWDdiurJan1.plot(ax=ax1, color='green',label='Land')

##axis 2 : April
MWDdiurApr0.plot(ax=ax2,color='blue', label='Lake')
MWDdiurApr1.plot(ax=ax2,color='green', label='Land')

ax1.legend(loc='top right', ncol=1, fancybox=True, shadow=True)
ax2.legend(loc='top right', ncol=1, fancybox=True, shadow=True)

ax1.set_title('diurnal variation of wind direction in January')
ax2.set_title('diurnal variation of wind direction in April')


#fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\Diurnal\diurnalWindDir.png', dpi=300)
#plt.clf()

