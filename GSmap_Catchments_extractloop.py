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
import geopandas as gpd
from datetime import timedelta, date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import xarray as xr
from netCDF4 import Dataset
import rasterio
from rasterstats import zonal_stats
from affine import Affine
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling
from rasterio import transform

#%% 
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

#%%
nc=xr.open_dataset(r'D:\DATA_ncdf\GSMaps\GSmap_crop_merged.nc')           # crop and concatenated GSmap file
Catchments= gpd.read_file('D:\QGIS_Malawi\RQ2_dynamic\Catchment_Karonga_WGS84.shp')

df= pd.DataFrame(np.empty([12, 18]))
df.loc[:,:]=0

#%% cumulative rain over the events
for i in range(len(FF_list)):   
    print(i)
    
    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
    endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
    
    cum_rain_event= nc['Gauge-calibratedRain'].sel(time=slice(startevent,endevent))
    cum_rain_event= cum_rain_event.sum(dim='time')
    
    # resampling of the map in higher resolution
    source= np.flip(cum_rain_event.values,0)
    destination =np.empty(shape=( 40 * 10, 40 * 10))
    src_transform = from_bounds(32, -12, 36,-8, 40, 40)
    dst_transform = from_bounds(32, -12, 36,-8, 40 * 10, 40 * 10)
    reproject(source, destination, 
             src_transform = src_transform, dst_transform = dst_transform, 
             src_crs = {'init': 'epsg:4326'}, dst_crs = {'init': 'epsg:4326'}, resampling = Resampling.nearest)
    
    # computing the statistic with the resampled tif 
    stats = zonal_stats(Catchments, destination, stats= 'mean', all_touched=True,affine= dst_transform, nodata= -999)
    
    # writting the statistics in the dataframe
    df.loc[:,i]= pd.DataFrame.from_dict(stats).loc[:,'mean']

df.to_csv('D:\Msc_Research\RQ2_DataAnalysis\GSMap\Cum_rain_events.csv')

#%% maximum peak of rain over the events
for i in range(len(FF_list)):   
    print(i)
    
    startevent = dt.datetime(year=FF_list.startYear[i], month=FF_list.startMonth[i], day=FF_list.startDay[i], hour=FF_list.startHr[i])
    endevent = dt.datetime(year=FF_list.endYear[i], month=FF_list.endMonth[i], day=FF_list.endDay[i], hour=FF_list.endHr[i])
    
    Max_rain_event= nc['Gauge-calibratedRain'].sel(time=slice(startevent,endevent))
    Max_rain_event= Max_rain_event.max(dim='time')
    
    # resampling of the map in higher resolution
    source= np.flip(Max_rain_event.values,0)
    destination =np.empty(shape=( 40 * 10, 40 * 10))
    src_transform = from_bounds(32, -12, 36,-8, 40, 40)
    dst_transform = from_bounds(32, -12, 36,-8, 40 * 10, 40 * 10)
    reproject(source, destination, 
             src_transform = src_transform, dst_transform = dst_transform, 
             src_crs = {'init': 'epsg:4326'}, dst_crs = {'init': 'epsg:4326'}, resampling = Resampling.nearest)
    
    # computing the statistic with the resampled tif 
    stats = zonal_stats(Catchments, destination, stats= 'mean', all_touched=True,affine= dst_transform, nodata= -999)
    
    # writting the statistics in the dataframe
    df.loc[:,i]= pd.DataFrame.from_dict(stats).loc[:,'mean']

df.to_csv('D:\Msc_Research\RQ2_DataAnalysis\GSMap/Max_rain_events.csv')

