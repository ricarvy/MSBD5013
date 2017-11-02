import os
working_directory = 'demo3'
os.chdir(working_directory)
from strategy import handle_bar

# Run the main function in your demo.py to get your model and training reday(if there is any)
os.system('python strategy.py')

import h5py
import pandas as pd
import numpy as np
import train
import matplotlib.pyplot as plt
# All data directory
# PnL plot, drawdown analysis and risk analysis
import pyfolio as pf
data_directory = '../Data/'
format1_dir = 'data_format1_20170717_20170915.h5'
format2_dir = 'data_format2_20170717_20170915.h5'
format2_list=['data_format2_20170717_20170915.h5',
              'data_format2_20170918_20170922.h5',
              'data_format2_20170925_20170929.h5',
              'data_format2_20171009_20171013.h5',
              'data_format2_20171016_20171020.h5']
import copy

data_format_path = data_directory+format2_dir
btData_train=h5py.File(data_format_path, mode='r')
keys = list(btData_train.keys())

def index_trasaction(df):
    df['open']=df[0]
    df['high']=df[1]
    df['low']=df[2]
    df['close']=df[3]
    df['volume']=df[4]
    df.drop([0,1,2,3,4], axis=1, inplace=True)

    df['mean_price'] = (df['open']+df['high']+df['low']+df['close'])/4
    #df.drop(['close'], 1, inplace=True)
    return df

def format_trasaction(bdData_train):
    total_list = list()
    for i in range(13):
        sample_list = list()
        for j in range(len(keys)):
            data_cur_min = btData_train[keys[j]][i]
            sample_list.append(data_cur_min)
        total_list.append(sample_list)
    return total_list

format1_list=format_trasaction(bdData_train=btData_train)

series_list=[]
newp_list=[]
newy_test_list=[]
train_score_list=[]
for i in range(len(format1_list)):
    stock_list=format1_list[i]
    for i in range(len(stock_list)):
        series=pd.Series(np.array(stock_list[i]))
        series_list.append(series)
    df=pd.DataFrame(series_list)

    df=index_trasaction(df)
    df_temp=df

    df=train.normalize_data(df)
    df_temp=train.normalize_data(df_temp)

    window=22
    X_train,y_train,X_test,y_test=train.load_data(df,window)

    model=train.build_model([6,window,1])

    print('No ',i,'model is training...')
    ### start training
    model.fit(X_train,y_train,batch_size=512,epochs=10,validation_split=0.1,verbose=1)

    diff=[]
    ratio=[]
    p=model.predict(X_test)
    print(p.shape)
    for u in range(len(y_test)):
        pr=p[u][0]
        ratio.append((y_test[u]/pr)-1)
        diff.append(abs(y_test[u]-pr))

    newp=train.denormalize(df_temp,p)
    newy_test=train.denormalize(df_temp,y_test)
    newp_list.append(newp)
    newy_test_list.append(newy_test)

    score=train.model_score(model,X_train,y_train,X_test,y_test)
    train_score_list.append(score)
    series_list=[]

# plt.plot(newp,color='red',label='Prediction')
# plt.plot(newy_test,color='blue',label='Actual')
# plt.legend(loc='best')
# plt.show()

