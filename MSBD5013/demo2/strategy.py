# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 22:46:03 2017

@author: MAngO
"""

asset_index = 2 # i.e. AU.SHF

def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):
    ''' Params: timer = int, counter of current time
        data = pandas.dataframe, data for current minute bar
        info - pandas.dataframe, information matrix
        init_cash，transaction - double, constans
        detail_last_min - list, contains cash balance, margin balance, total balance and position of last minute
        memory - class, current memory of your strategy
    '''
    
    # Basically this strategy long 1 lot of AU.SHF every minute until system stops 
    # (cash balance is lower than cash balance lower limit) so you can get a bit of sense 
    # about leverage and risk control
    position_new = detail_last_min[0]
    position_new[asset_index] += 1.
    
    return position_new, memory

if __name__ == '__main__':
    ''' This strategy simply check if there is any special technical pattern in data
        No training process required. Main function is passed.
    '''
    pass