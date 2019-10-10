# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 18:20:12 2019

@author: Dr Sam Hollings
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def plot_uk_basemap(ax=None,map_kwargs=None):
    # these lat and long give a decent map of England
    map_box_width = 8.9
    map_box_height = 6.3
    lat_c = 52.8#54.5
    lon_c = -2#-4.36
    
    # 
    map = Basemap(projection='merc',
                lat_0=lat_c, lon_0=lon_c,
                llcrnrlon=lon_c-map_box_width/2,#=#-6., 
                llcrnrlat=lat_c-map_box_height/2, #49.5, 
                urcrnrlon=lon_c+map_box_width/2,#lon_c+map_box_size/22,#., 
                urcrnrlat=lat_c+map_box_height/2,#59,#55.2,
                resolution='l', ax=ax)
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    #map.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
    map.drawmapboundary(fill_color='white')
    return map

# apply ccgs to the map
#map.readshapefile('ccg_2019\ccg_2019', # location of the files (leave out extensions)
                  #'ccg') # this is what this is referred to in the "map" object

# let's make some random data for each ccg
df_ccg = pd.DataFrame(map.ccg_info).set_index('ccg19cd')

import numpy.random as npr
df_ccg['random'] = npr.rand(len(df_ccg))

def colour_regions(df_ccg_geog_values, column,map=None, num_colours=10, cm=plt.get_cmap('Blues')):
    # this takes the df and applies the values in the "column" as colours on a chloropleth map
    # the df must have geography codes corresponding with the shapefile read into the map.
    # the index of the dataframe must be the right sort of code. i.e. ONS CCG code if using an ONS shapefile
    
    if map is None:
        fig,ax = plt.subplots(figsize=(25,20))
        map = plot_uk_basemap(ax=ax)
        map.readshapefile('ccg_2019\ccg_2019', 'ccg') # this is what this is referred to in the "map" object
    
    # sample the colours for the the number we have from the colour map
    scheme = [cm(i / num_colours) for i in range(num_colours)]
    
    # let's group the data into bins corresponding to the colour levels)
    bins = np.linspace(df_ccg_geog_values[column].min(), 
                       df_ccg_geog_values[column].max(), 
                       num_colours)
    
    df_ccg_geog_values['bin'] = np.digitize(df_ccg_geog_values[column], 
                                            bins) - 1
    
    # now compose the group of patches coloured by the bin
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    
    for info, shape in zip(map.ccg_info, map.ccg):
        color = scheme[df_ccg_geog_values.loc[info['ccg19cd']].bin.max()] # there is a max here to stop it breaking when CCG is duplicated
        patches = [Polygon(np.array(shape), True)]
        pc = PatchCollection(patches)
        pc.set_facecolor(color)
        ax.add_collection(pc)

colour_regions(df_ccg, 'random')

plt.show()
