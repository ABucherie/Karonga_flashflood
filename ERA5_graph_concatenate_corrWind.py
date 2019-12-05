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
import matplotlib.dates as mdates

#%% QUITE long to RUN !!
# open parameters  dataset
nct=xr.open_dataset(r'D:\DATA_ncdf/2mtemperature.nc')
ncc=xr.open_dataset(r'D:\DATA_ncdf/cape.nc')
ncv=xr.open_dataset(r'D:\DATA_ncdf/VolSoilWater.nc')
ncwU=xr.open_dataset(r'D:\DATA_ncdf/Uwind.nc')
ncwV=xr.open_dataset(r'D:\DATA_ncdf/Vwind.nc')
ncRH=xr.open_dataset(r'D:\DATA_ncdf/ERA5_RH500_850.nc')

#resampling
rt=nct.resample(time='1D').mean(dim='time')
rc=ncc.resample(time='1D').mean(dim='time')
rv=ncv.resample(time='1D').mean(dim='time')
rwU=ncwU.resample(time='1D').mean(dim='time')
rwV=ncwV.resample(time='1D').mean(dim='time')
rRH=ncRH.resample(time='1D').mean(dim='time')

#%%
# choosing the 2 locations 
lon_loc = [33.75, 34.00]  # North Karonga and  South Karonga locations
lat_loc = [-9.75, -10.25]    

#lon_loc = [34.25, 33.75]    # Lake and Land (mid Karonga) locations
#lat_loc = [-10, -10]

# create a date variable for the start of the timeperiod to analyse
startYear, startMonth,startDay, startHr = (2016,11,1,0)
endYear, endMonth,endDay, endHr = (2017,5,1,23)
startDate = dt.datetime(year=startYear, month=startMonth, day=startDay, hour=startHr)
endDate = dt.datetime(year=endYear, month=endMonth, day=endDay, hour=endHr)

#%% compute the grouping for the 20 years as baseline
# at the 2 X Y locations and for the defined timeslice

Tdeg = rt.t2m - 273.15
Temp0= Tdeg*0
Cape0=rc.cape*0
Vsw0=rv.swvl1*0
Uw0=rwU.u10*0
Vw0=rwV.v10*0
RH0=rRH.r*0

TempMean= Temp0.groupby('time.dayofyear')+Tdeg.groupby('time.dayofyear').mean('time')
RHMean= RH0.groupby('time.dayofyear')+rRH.r.groupby('time.dayofyear').mean('time')
CapeMean= Cape0.groupby('time.dayofyear')+rc.cape.groupby('time.dayofyear').mean('time')
SoilMMean= Vsw0.groupby('time.dayofyear')+rv.swvl1.groupby('time.dayofyear').mean('time')
Uwindmean=Uw0.groupby('time.dayofyear')+rwU.u10.groupby('time.dayofyear').mean('time')
Vwindmean=Vw0.groupby('time.dayofyear')+rwV.v10.groupby('time.dayofyear').mean('time')
WspeedMean= np.sqrt(Uwindmean**2+Vwindmean**2) 
WdirMean= (180/ np.pi) * np.arctan2(-Uwindmean,-Vwindmean)

#compute parameters, name and units
TempMean.attrs["units"], TempMean.attrs["long_name"] ='deg C', 'Temperature'
RHMean.attrs["units"], RHMean.attrs["long_name"] ='%', 'Rel. Humidity (500-850mb)'
CapeMean.attrs["units"], CapeMean.attrs["long_name"] ='J/kg', 'Cape'
SoilMMean.attrs["units"], SoilMMean.attrs["long_name"] ='m3/m3', 'Vol.Soil water'
WspeedMean.attrs["units"], WspeedMean.attrs["long_name"] ='m/s', 'Wind speed'
WdirMean.attrs["units"], WdirMean.attrs["long_name"] ='deg', 'Met. wind direction'

# extract mean parameters for the 2 locations for the given slice time
tm1 =TempMean.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
tm2 =TempMean.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
cm1 =CapeMean.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
cm2 =CapeMean.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
sm1 =SoilMMean.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
sm2 =SoilMMean.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
wm1=WspeedMean.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
wm2=WspeedMean.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate)) 
wd1=WdirMean.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
wd2=WdirMean.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
rh1= RHMean.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate)) 
rh2= RHMean.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
#%%create a graph with all parameters daily averaraged over the entire dataset of 20 years
#plotting all average parameters

fig = plt.figure(figsize=(13,13))

gs = gridspec.GridSpec(6,1) 
    
ax1=plt.subplot(gs[0,0])
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax2=plt.subplot(gs[1,0])
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax3=plt.subplot(gs[2,0])
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax4=plt.subplot(gs[3,0])
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax5=plt.subplot(gs[4,0])
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax6=plt.subplot(gs[5,0])
ax6.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

gs.update(wspace=0 ,hspace=0.7) 

#axis 1 : temperature
#tm1.plot(ax=ax1, color='blue', label='location A: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
#tm2.plot(ax=ax1, color='green', label='location B: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
tm1.plot(ax=ax1, color='blue', label='Lake: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
tm2.plot(ax=ax1, color='green', label='Land: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))

#axis 2 : RH
rh1.plot(ax=ax2, color='blue')
rh2.plot(ax=ax2, color='green')
#axis 3 : cape
cm1.plot(ax=ax3, color='blue')
cm2.plot(ax=ax3, color='green')
#axis 4 : volumetric soil water
sm1.plot(ax=ax4, color='blue')
sm2.plot(ax=ax4, color='green')
#axis 5 : Wind speed
wm1.plot(ax=ax5, color='blue')
wm2.plot(ax=ax5, color='green')
#axis 6 : meteorological wind direction
wd1.plot(ax=ax6, color='blue')
wd2.plot(ax=ax6, color='green')

ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')
ax5.set_title('')
ax6.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\WetSeasons\ERA5_avgParam_season_NS_withRH.png', dpi=300)
#plt.clf()

#%% compute parameters, name and units with resampled dataset for a speific season/month
# compute parameters, name and units with resampling dataset
rc.cape.attrs["units"], rc.cape.attrs["long_name"] ='J/kg', 'Cape'
rv.swvl1.attrs["units"], rv.swvl1.attrs["long_name"] ='m3/m3', 'Vol.Soil water'
rRH.r.attrs["units"], rRH.r.attrs["long_name"] ='%', 'Rel. humidity (500-850mb)'
# compute total Wind speed and meteorological wind direction
WM= np.sqrt(rwU.u10**2+rwV.v10**2)    # compute total Wind speed frm resampled u and v
WM.attrs["units"], WM.attrs["long_name"] ='m/s', 'Wind speed'
MWD= (180/ np.pi) * np.arctan2(-rwU.u10,-rwV.v10)      # compute total meteorological wind direction from -180 to 180
#MWD= 180+ (180/ np.pi) * np.arctan2(ncwU.u10,ncwV.v10)      # compute total meteorological wind direction from 0 to 360
MWD.attrs["units"], MWD.attrs["long_name"] ='deg', 'Met. wind direction'
# Convert to celsius and change labels from Kelvin to Celsius
Tdeg = rt.t2m - 273.15
Tdeg.attrs["units"], Tdeg.attrs["long_name"] ='deg C', 'Temperature'

# extract temperature for the 2 locations for the given slice time
nct1 =Tdeg.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
nct2 =Tdeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
# extract RH for the 2 locations for the given slice time
ncrh1= rRH.r.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate)) 
ncrh2= rRH.r.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
# extract cape  for the 2 locations for the given slice time
ncc1 =rc.cape.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
ncc2 =rc.cape.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
# extract volumetric soil water  for the 2 locations for the given slice time
ncv1 =rv.swvl1.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
ncv2 =rv.swvl1.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
# Extract wind speed and meteorological wind direction
ncWM1=WM.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
ncWM2=WM.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate)) 
ncWD1=MWD.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
ncWD2=MWD.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))

# plotting a time serie at 2 X Y locations
fig = plt.figure(figsize=(13,13))

gs = gridspec.GridSpec(6,1) 
ax1=plt.subplot(gs[0,0])
ax2=plt.subplot(gs[1,0])
ax3=plt.subplot(gs[2,0])
ax4=plt.subplot(gs[3,0])
ax5=plt.subplot(gs[4,0])
ax6=plt.subplot(gs[5,0])
gs.update(wspace=0 ,hspace=0.8) 

#axis 1 : temperature
nct1.plot(ax=ax1, color='blue', label='location A: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
nct2.plot(ax=ax1, color='green', label='location B: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
#nct2.plot(ax=ax1, color='blue', label='Lake: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
#nct2.plot(ax=ax1, color='green', label='Land: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
tm1.plot(ax=ax1, linestyle='--', color='blue')
tm1.plot(ax=ax1, linestyle='--',color='blue')

#axis 2 : RH
ncrh1.plot(ax=ax2, color='blue')
ncrh2.plot(ax=ax2, color='blue')
rh1.plot(ax=ax2, linestyle='--', color='blue')
rh2.plot(ax=ax2, linestyle='--', color='green')

#axis 3 : cape
ncc1.plot(ax=ax3, color='blue')
ncc2.plot(ax=ax3, color='green')
cm1.plot(ax=ax3,linestyle='--', color='blue')
cm2.plot(ax=ax3,linestyle='--', color='green')

#axis 4 : volumetric soil water
ncv1.plot(ax=ax4, color='blue')
ncv2.plot(ax=ax4, color='green')
sm1.plot(ax=ax4,linestyle='--', color='blue')
sm2.plot(ax=ax4,linestyle='--', color='green')

#axis 5 : Wind speed
ncWM1.plot(ax=ax5, color='blue')
ncWM2.plot(ax=ax5, color='green')
wm1.plot(ax=ax5,linestyle='--', color='blue')
wm2.plot(ax=ax5,linestyle='--', color='green')

#axis 6 : meteorological wind direction
ncWD1.plot(ax=ax6, color='blue')
ncWD2.plot(ax=ax6, color='green')
wd1.plot(ax=ax6,linestyle='--', color='blue')
wd2.plot(ax=ax6, linestyle='--',color='green')


ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.7), ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')
ax5.set_title('')
ax6.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\WetSeasons\ERA5_20162017_RH_wBase.png', dpi=300)
#plt.clf()


#%%
# compute parameters, name and units with normal (non resampled) dataset, for a specific event, and plotting against the baseline of the 20 years averaged

ncc.cape.attrs["units"],ncc.cape.attrs["long_name"] ='J/kg', 'Cape'
ncv.swvl1.attrs["units"], ncv.swvl1.attrs["long_name"] ='m3/m3', 'Vol.Soil water'
# compute total Wind speed and meteorological wind direction
WM= np.sqrt(ncwU.u10**2+ncwV.v10**2)    # compute total Wind speed
WM.attrs["units"], WM.attrs["long_name"] ='m/s', 'Wind speed'
MWD= (180/ np.pi) * np.arctan2(-ncwU.u10,-ncwV.v10)      # compute total meteorological wind direction from -180 to 180
#MWD= 180+ (180/ np.pi) * np.arctan2(ncwU.u10,ncwV.v10)      # compute total meteorological wind direction from 0 to 360
MWD.attrs["units"], MWD.attrs["long_name"] ='deg', 'Met. wind direction'
# Convert to celsius and change labels from Kelvin to Celsius
Tdeg = nct.t2m - 273.15
Tdeg.attrs["units"], Tdeg.attrs["long_name"] ='deg C', 'Temperature'

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
#nct1.plot(ax=ax1, color='blue', label='location A: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
#nct2.plot(ax=ax1, color='green', label='location B: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
nct2.plot(ax=ax1, color='blue', label='Lake: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
nct2.plot(ax=ax1, color='green', label='Land: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
tm1.plot(ax=ax1, linestyle='--', color='blue')
tm2.plot(ax=ax1, linestyle='--',color='blue')

#axis 2 : cape
ncc1.plot(ax=ax2, color='blue')
ncc2.plot(ax=ax2, color='green')
cm1.plot(ax=ax2,linestyle='--', color='blue')
cm2.plot(ax=ax2,linestyle='--', color='green')

#axis 3 : volumetric soil water
ncv1.plot(ax=ax3, color='blue')
ncv2.plot(ax=ax3, color='green')
sm1.plot(ax=ax3,linestyle='--', color='blue')
sm2.plot(ax=ax3,linestyle='--', color='green')

#axis 4 : Wind speed
ncWM1.plot(ax=ax4, color='blue')
ncWM2.plot(ax=ax4, color='green')
wm1.plot(ax=ax4,linestyle='--', color='blue')
wm2.plot(ax=ax4,linestyle='--', color='green')

#axis 5 : meteorological wind direction
ncWD1.plot(ax=ax5, color='blue')
ncWD2.plot(ax=ax5, color='green')
wd1.plot(ax=ax5,linestyle='--', color='blue')
wd2.plot(ax=ax5, linestyle='--',color='green')


ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.5), ncol=1, fancybox=True, shadow=True)
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
ax4.set_title('')

fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\WetSeasons\Jan2015_withbaseline.png', dpi=300)
plt.clf()
