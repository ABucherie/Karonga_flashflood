# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 16:21:46 2017

@author: Agathe Bucherie
"""

'''
The script is done to extract maximum and mean values of Cape over 4 different regions in North Malawi, 3 days before the Flash Flood events strarts

'''
#%%
import datetime as dt   # Python standard library datetime  module
from datetime import timedelta, date
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import xarray as xr
#from netCDF4 import Dataset

#%%
ncRH=xr.open_dataset(r'D:\DATA_ncdf/ERA5_RH500_850.nc')
 
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


#%% cape mean and max per region

RH_reg=np.empty([18, 8])

for i in range(len(FF_list)):    # or calcutate over a loop for all events
    print(i)
    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
    #South region
    ncRH_S=ncRH.r.sel(longitude= slice(34.25,34.5), latitude=slice(-10,-11.5),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_Sevent=ncRH_S.mean()
    Cmax_Sevent=ncRH_S.max()
    #West region
    ncRH_W=ncRH.r.sel(longitude= slice(33.25,34), latitude=slice(-9.75,-11.25),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_Wevent=ncRH_W.mean()
    Cmax_Wevent=ncRH_W.max()
    #NW region
    ncRH_NW=ncRH.r.sel(longitude= slice(32,33.5), latitude=slice(-8,-9.5),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_NWevent=ncRH_NW.mean()
    Cmax_NWevent=ncRH_NW.max()    
    #NE region
    ncRH_NE=ncRH.r.sel(longitude= slice(34.5,36), latitude=slice(-8,-9.5),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_NEevent=ncRH_NE.mean()
    Cmax_NEevent=ncRH_NE.max() 
    
    RH_reg[i] = [Cmean_Sevent,Cmax_Sevent,Cmean_Wevent,Cmax_Wevent,Cmean_NWevent,Cmax_NWevent,Cmean_NEevent, Cmax_NEevent ]

np.savetxt('D:\Msc_Research\RQ2_DataAnalysis\ERA_5/RH1d_regio.csv', RH_reg, delimiter=",")


#%% RHresampled in region West from 1 to 3 days to check the variation and quantile P90
ncRH=xr.open_dataset(r'D:\DATA_ncdf/ERA5_RH500_850.nc')
#ncRH=ncRH.r.sel(longitude= slice(33.25,34), latitude=slice(-9.75,-11.25))     # west region
#ncRH=ncRH.r.sel(longitude= slice(34.25,34.5), latitude=slice(-10,-11.5))    # south region
#ncRH=ncRH.r.sel(longitude= slice(32,33.5), latitude=slice(-8,-9.5))   # NW region
ncRH=ncRH.r.sel(longitude= slice(34.5,36), latitude=slice(-8,-9.5))    # NEregion

RH_res_max=ncRH.resample(time='1D').max()
RH_res_mean=ncRH.resample(time='1D').mean()

startYear, startMonth,startDay, startHr = (2011,5,1,0)
endYear, endMonth,endDay, endHr = (2012,5,1,23)
startDate = dt.datetime(year=startYear, month=startMonth, day=startDay, hour=startHr)
endDate = dt.datetime(year=endYear, month=endMonth, day=endDay, hour=endHr)

wetseason = [12,1,2,3,4]

RH_max_wetseason= RH_res_max.where(RH_res_max['time.month'].isin(wetseason))
RH_mean_wetseason= RH_res_mean.where(RH_res_mean['time.month'].isin(wetseason))
#RH_max_wetseason.sel(time = slice(startDate,endDate)).plot()
print (RH_max_wetseason.quantile(0.4))
print (RH_mean_wetseason.quantile(0.4))
print (RH_max_wetseason.quantile(0.6))
print (RH_mean_wetseason.quantile(0.6))
print (RH_max_wetseason.quantile(0.9))
print (RH_mean_wetseason.quantile(0.9))