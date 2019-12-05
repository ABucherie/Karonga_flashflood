# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 16:21:46 2017

@author: Agathe Bucherie
"""

'''
The script is a test to try to read NCDF file and to plot timeline of ERA5 parameters

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
ncd=xr.open_dataset(r'D:\DATA_ncdf/DewPointTemperature.nc')
ncRH=xr.open_dataset(r'D:\DATA_ncdf/ERA5_RH500_850.nc')

# compute total Wind speed and meteorological wind direction
WM= np.sqrt(ncwU.u10**2+ncwV.v10**2)    # compute total Wind speed
WM.attrs["units"], WM.attrs["long_name"] =ncwU.u10.attrs["units"], 'Wind speed'
MWD= (180/ np.pi) * np.arctan2(-ncwU.u10,-ncwV.v10)      # compute total meteorological wind direction
MWD.attrs["units"], MWD.attrs["long_name"] ='deg', 'meteorological wind direction'

# Convert to celsius and change labels from Kelvin to Celsius
Tdeg = nct.t2m - 273.15
Tdeg.attrs = nct.t2m.attrs
Tdeg.attrs['units'] = 'deg C'

Tddeg = ncd.d2m - 273.15
Tddeg.attrs = ncd.d2m.attrs
Tddeg.attrs['units'] = 'deg C'

#%%
# choosing the 2 locations North and South
lon_loc = [33.75, 34.00]
lat_loc = [-9.75, -10.25]

# choosing the 2 locations Lake and Land
#lon_loc = [34.25, 33.75]
#lat_loc = [-10, -10]

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
#definition of the time period to analyse in the graph
tp = np.array([['','startYear','startMonth','startDay', 'startHr','endYear','endMonth','endDay', 'endHr' ],
                   ['Event0',2018,4,5,0,    2018,4,12,23], 
                   ['Event1',2018,1,26,0,   2018,2,1,23], 
                   ['Event2',2018,1,17,0,   2018,1,23,23],
                   ['Event3',2018,1,7,0,    2018,1,14,23], 
                   ['Event4',2017,3,26,0,   2017,4,5,23 ],
                   ['Event5',2017,1,1,0,    2017,1,7,23],
                   ['Event6',2016,2,24,0,   2016,3,2,23],
                   ['Event7',2016,1,26,0,   2016,2,2,23], 
                   ['Event8',2015,1,14,0,   2015,1,20,23],
                   ['Event9',2014,12,28,0,  2015,1,4,23],
                   ['Event10',2014,3,14,12, 2014,3,20,23],
                   ['Event11',2014,2,19,12, 2014,2,25,23],
                   ['Event12',2014,1,25,12,  2014,1,31,23],
                   ['Event13',2013,3,21,12,  2013,3,27,23],
                   ['Event14',2009,3,4,12,   2009,3,9,23],
                   ['Event15',2007,1,17,12,  2007,1,23,23],
                   ['Event16',2006,4,1,12,   2006,4,6,23],
                   ['Event17',2004,1,22,12,  2004,1,28,23]])

TimePeriod= pd.DataFrame(data=tp[1:,1:], index=tp[1:,0], columns=tp[0,1:])
TimePeriod= TimePeriod.astype('int64')

#%%
#i=17  # choose the event to evaluate
for i in range(len(FF_list)):    # or calcutate over a loop for all events
    print(i)
    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
    endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
    startDate = dt.datetime(year=TimePeriod.startYear[i], month=TimePeriod.startMonth[i], day=TimePeriod.startDay[i], hour=TimePeriod.startHr[i])
    endDate = dt.datetime(year=TimePeriod.endYear[i], month=TimePeriod.endMonth[i], day=TimePeriod.endDay[i], hour=TimePeriod.endHr[i])
    
    # extract temperature for the 2 locations for the given slice time
    nct1 =Tdeg.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
    nct2 =Tdeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
    
    # extract due point temperature  for the 2 locations for the given slice time
    ncd1 =Tddeg.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
    ncd2 =Tddeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
    
    # extract relative humidity  for the 2 locations for the given slice time
    ncRH1=ncRH.r.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
    ncRH2=ncRH.r.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
    
    # extract cape  for the 2 locations for the given slice time
    ncc1 =ncc.cape.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))   
    ncc2 =ncc.cape.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
    
    # Extract wind speed and meteorological wind direction
    ncWM1=WM.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
    ncWM2=WM.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate)) 
    ncWD1=MWD.sel(longitude=lon_loc[0],latitude=lat_loc[0], time=slice(startDate,endDate))  
    ncWD2=MWD.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startDate,endDate))
    
    #create the timestamps for FF events
    EventT=Tdeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(nct1.max(), nct2.max())
    EventT.attrs["units"], EventT.attrs["long_name"] =nct1.attrs["units"], nct1.attrs["long_name"]
    EventD=Tddeg.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncd1.max(), ncd2.max())+0.05
    EventD.attrs["units"], EventD.attrs["long_name"] =ncd1.attrs["units"], ncd1.attrs["long_name"]
    EventR=ncRH.r.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncRH1.max(), ncRH2.max())
    EventR.attrs["units"], EventR.attrs["long_name"] =ncRH.attrs["units"], ncRH.attrs["long_name"]
    EventC=ncc.cape.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncc1.max(), ncc2.max())
    EventC.attrs["units"], EventC.attrs["long_name"] =ncc1.attrs["units"], ncc1.attrs["long_name"]
    EventWM=WM.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncWM1.max(), ncWM2.max()) +0.5
    EventWM.attrs["units"], EventWM.attrs["long_name"] =ncWM1.attrs["units"], ncWM1.attrs["long_name"]
    EventWD=MWD.sel(longitude=lon_loc[1],latitude=lat_loc[1], time=slice(startevent,endevent))*0 + max(ncWD1.max(), ncWD1.max())+ 20
    EventWD.attrs["units"], EventWD.attrs["long_name"] =ncWD1.attrs["units"], ncWD1.attrs["long_name"]
    
    # plotting a time serie at 2 X Y locations with the parameter we want 
    
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
#    nct1.plot(ax=ax1, color='blue', label='location Lake: lat  '+ str(lat_loc[0])+' /  lon '+str(lon_loc[0]))
#    nct2.plot(ax=ax1, color='green', label='location Land: lat '+ str(lat_loc[1])+' / lon '+str(lon_loc[1]))
    EventT.plot(ax=ax1, color='red', linewidth=5)
    
    #axis 2 : dew point temerature or relative humidity for plot number 2
#    ncd1.plot(ax=ax2, color='blue')
#    ncd2.plot(ax=ax2, color='green')
#    EventD.plot(ax=ax2, color='red', linewidth=5)
    ncRH1.plot(ax=ax2, color='blue')
    ncRH2.plot(ax=ax2, color='green')
    EventR.plot(ax=ax2, color='red', linewidth=5)
    
    #axis 3 : cape
    ncc1.plot(ax=ax3, color='blue')
    ncc2.plot(ax=ax3, color='green')
    EventC.plot(ax=ax3, color='red', linewidth=5)
    
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
    
    fig.savefig('D:\Python_Scripts_Malawi\Results_ERA5\Graph_dewpoint_RH\graph_event'+str(i)+'_2locNS.png', dpi=300)
    plt.clf()


