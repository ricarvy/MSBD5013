#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:27:48 2017

@author: MAngO
"""
import numpy as np
# Here we use technical analysis functions written by ourselves. If you want to use
# packages like TA-Lib, you need to follow the installation guidance down below:
# https://mrjbq7.github.io/ta-lib/install.html
from auxiliary import generate_bar, white_soider, black_craw

''' You can define variables that your strategy may use during the backtesting process here
'''
bar_length = 15 # Number of minutes to generate next new bar
asset_index = 2 # Index of asset you want to use in this strategy, e.g. AU
my_cash_balance_lower_limit = 3000000. # Cutting-loss criterion

def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    ''' Params: timer = int, counter of current time
        data = pandas.dataframe, data for current minute bar
        info - pandas.dataframe, information matrix
        init_cash，transaction - double, constans
        detail_last_min - list, contains cash balance, margin balance, total balance and position of last minute
        memory - class, current memory of your strategy
    '''
    # Get position of last minute
    position_new = detail_last_min[0]
    
    # Generate OHLC data for every 15 minutes
    if(timer==0):
        memory.data_list = list()
        memory.bar_prev = np.array([None])
        memory.ws_check_table = np.empty((0,2))
        memory.bc_check_table = np.empty((0,2))
        memory.long_stop_loss = np.inf
        memory.long_profit_target = np.inf
        memory.short_stop_loss = np.inf
        memory.short_profit_target = np.inf
    
    if(timer%bar_length==0 and timer!=0):
        memory.data_list.append(data)
        bar = generate_bar(memory.data_list)
        memory.data_list = list() # Clear memory.data_list after bar combination
        
        if memory.bar_prev.any()!=None:
            ws_check = white_soider(bar, memory.bar_prev, asset_index)
            memory.ws_check_table = np.append(memory.ws_check_table, [ws_check], axis=0)
            bc_check = black_craw(bar, memory.bar_prev, asset_index)
            memory.bc_check_table = np.append(memory.bc_check_table, [bc_check], axis=0)
            
        bar_num = len(memory.ws_check_table)
        if bar_num>3:
            ''' long signal 
                When there is a three white soider signal, long 10 lots of asset at next minute unless 
                the current cash balance is less than 3,000,000
            '''
            if np.sum(memory.ws_check_table[bar_num-3:bar_num,1])==3:
                if detail_last_min[1] > my_cash_balance_lower_limit:
                    position_new[asset_index] += 10.
                    memory.long_stop_loss = memory.ws_check_table[bar_num-3,0]
                    memory.long_profit_target = memory.ws_check_table[bar_num-1,0]*(1+.05)
            
            ''' short signal 
                When there is a three black craw signal, short 10 lots of asset at next minute unless 
                the current cash balance is less than 3,000,000
            '''
            if np.sum(memory.bc_check_table[bar_num-3:bar_num,1])==2:
                if detail_last_min[1] > my_cash_balance_lower_limit:
                    position_new[asset_index] -= 10.
                    memory.short_stop_loss = memory.bc_check_table[bar_num-3,0]
                    memory.short_profit_target = memory.bc_check_table[bar_num-1,0]*(1+.05)
        
        memory.bar_prev = bar
        
    # save minute data to data_list
    else:
        memory.data_list.append(data)
    
    # Close signal
    # When reach stop loss/target profit points, clear all long/short positions
    average_price = np.mean(data[asset_index,:4])
    if(position_new[asset_index] > 0):
        if average_price > memory.long_profit_target or average_price < memory.long_stop_loss:
            position_new[asset_index] = 0.
    else:
        if average_price > memory.short_stop_loss or average_price < memory.short_profit_target:
            position_new[asset_index] = 0.
    # End of strategy
    return position_new, memory
    
if __name__ == '__main__':
    ''' This strategy simply check if there is any special technical pattern in data
        No training process required. Main function is passed.
    '''
    pass