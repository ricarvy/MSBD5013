#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:27:48 2017

@author: MAngO
"""
import numpy as np

def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    ''' Strategy that buy and hold, always hold AU futures contract with half of your capital
    '''
    index = 2 # i.e. AU.SHF, here index is 2 because index of python list starts from 0
    
    # Get execution price of this minute
    avag_price = np.mean(data[index,:4])
    
    # Get the value of one lot so that you can get how many lots you can buy in total
    lot_value = avag_price * info.unit_per_lot[index] * info.margin_rate[index]
    
    # Prepare the position matrix
    position = np.repeat(0.,data.shape[0])
    # Change the corresponding entry(here is the entry of AU) to the number of lots you need to buy
    position[index] = np.round(0.5*init_cash/(lot_value*(1.+transaction)))
    
    # This simple strategy doesn't need any memory parameters, so we just return empty list 
    return position,memory

def train(*args, **kwargs):
    ''' If your strategy needs training process, please write training function here and run it in main 
    '''
    pass

if __name__ == '__main__':
    print('Hello!\nThis demo needs no model so there is no training here')
    import time
    time.sleep(5)