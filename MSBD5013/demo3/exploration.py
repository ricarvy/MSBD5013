# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:56:58 2017

@author: MAngO
"""

''' This file contains auxiliary functions for strategy.py and handel_bar()
You can also visualize the data here to get a sense about its trend and distribution.
This may help you when developing the strategy
'''

import os
working_directory = '/Users/MAngO/Dropbox/MAFS&MSBD/MSBD 5013/Python Platform/demo3'
os.chdir(working_directory)

# Get data
import h5py
import pandas as pd
data_directory = '/Users/MAngO/Dropbox/MAFS&MSBD/MSBD 5013/Python Platform/Data/'
format1 = pd.HDFStore(data_directory+'data_format1_20170717_20170915.h5', mode='r')
format2 = h5py.File(data_directory+'data_format2_20170717_20170915.h5', mode='r')

# Get all min data from format2
min_data = [item[1][:] for item in list(format2.items())]

# Visualize data in the form of candel chart
from auxiliary import plot_candles
AU = format1['AU.SHF']
AU_min = AU[:100]
AU_15min = pd.concat([AU[:600].open.resample('15min').first(),
                      AU[:600].high.resample('15min').max(),
                      AU[:600].low.resample('15min').min(),
                      AU[:600].close.resample('15min').last(),
                      AU[:600].volume.resample('15min').sum()],axis=1).dropna()

plot_candles(AU_min, volume_bars=True, title='AU 1-min Candle Chart')
plot_candles(AU_15min, volume_bars=True, title='AU First 15-min Candle Chart')


# Function test of bar combination, white soider pattern and black craw pattern
from auxiliary import generate_bar, white_soider, black_craw

# Bar combination test
print('Combine first 15min data into one bar:')
print(generate_bar(min_data[:15]))

# White soider pattern test
print('\nTest is 15-30min and 0-15min form white soider:')
print(white_soider(generate_bar(min_data[15:30]), generate_bar(min_data[:15]))[1])

# Black craw pattern test
print('\nTest is 15-30min and 0-15min form black craw:')
print(black_craw(generate_bar(min_data[15:30]), generate_bar(min_data[:15]))[1])