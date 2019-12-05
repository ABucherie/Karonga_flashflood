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
ncc=xr.open_dataset(r'D:\DATA_ncdf/cape.nc')
 
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

Cape_reg=np.empty([18, 8])

for i in range(len(FF_list)):    # or calcutate over a loop for all events
    print(i)
    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
    #South region
    ncc_S=ncc.cape.sel(longitude= slice(34.25,34.5), latitude=slice(-10,-11.5),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_S3d=ncc_S.mean()
    Cmax_S3d=ncc_S.max()
    #West region
    ncc_W=ncc.cape.sel(longitude= slice(33.25,34), latitude=slice(-9.75,-11.25),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_W3d=ncc_W.mean()
    Cmax_W3d=ncc_W.max()
    #NW region
    ncc_NW=ncc.cape.sel(longitude= slice(32,33.5), latitude=slice(-8,-9.5),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_NW3d=ncc_NW.mean()
    Cmax_NW3d=ncc_NW.max()    
    #NE region
    ncc_NE=ncc.cape.sel(longitude= slice(34.5,36), latitude=slice(-8,-9.5),time=slice(startevent-timedelta(days=1),startevent))
    Cmean_NE3d=ncc_NE.mean()
    Cmax_NE3d=ncc_NE.max() 
    
    Cape_reg[i] = [Cmean_S3d,Cmax_S3d,Cmean_W3d,Cmax_W3d,Cmean_NW3d,Cmax_NW3d,Cmean_NE3d, Cmax_NE3d ]

np.savetxt('D:\Msc_Research\RQ2_DataAnalysis\ERA_5/Cape1d_regio.csv', Cape_reg, delimiter=",")


#%% cape resampled in region West from 1 to 3 days to check the variation and quantile P90
ncc=xr.open_dataset(r'D:\DATA_ncdf/cape.nc')
#ncc=ncc.cape.sel(longitude= slice(33.25,34), latitude=slice(-9.75,-11.25))     # west region
#ncc=ncc.cape.sel(longitude= slice(34.25,34.5), latitude=slice(-10,-11.5))    # south region
#ncc=ncc.cape.sel(longitude= slice(32,33.5), latitude=slice(-8,-9.5))   # NW region
ncc=ncc.cape.sel(longitude= slice(34.5,36), latitude=slice(-8,-9.5))    # NEregion
cape_res_max=ncc.resample(time='3D').max()
cape_res_mean=ncc.resample(time='3D').mean()

startYear, startMonth,startDay, startHr = (2017,6,1,0)
endYear, endMonth,endDay, endHr = (2018,6,1,23)
# create a date variable for the start of the timeperiod to analyse
startDate = dt.datetime(year=startYear, month=startMonth, day=startDay, hour=startHr)
endDate = dt.datetime(year=endYear, month=endMonth, day=endDay, hour=endHr)

wetseason = [12,1,2,3,4]
EarlyWS = [12,1,2]
LateWS =[3,4]

C_max_wetseason= cape_res_max.where(cape_res_max['time.month'].isin(wetseason))
C_mean_wetseason= cape_res_mean.where(cape_res_max['time.month'].isin(wetseason))

#cape_res_max.sel(time = slice(startDate,endDate)).plot()
print (C_max_wetseason.quantile(0.4))
print (C_mean_wetseason.quantile(0.4))
print (C_max_wetseason.quantile(0.6))
print (C_mean_wetseason.quantile(0.6))
print (C_max_wetseason.quantile(0.9))
print (C_mean_wetseason.quantile(0.9))