import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import datetime
from sklearn import preprocessing
import datetime
from operator import itemgetter
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation
from keras.layers.recurrent import LSTM
from keras.models import load_model
import os
import math,time

def normalize_data(df):
    min_max_scaler=preprocessing.MinMaxScaler()
    df['open']=min_max_scaler.fit_transform(df.open.values.reshape(-1,1))
    df['high']=min_max_scaler.fit_transform(df.high.values.reshape(-1,1))
    df['low']=min_max_scaler.fit_transform(df.low.values.reshape(-1,1))
    df['volume']=min_max_scaler.fit_transform(df.volume.values.reshape(-1,1))
    df['mean_price']=min_max_scaler.fit_transform(df['mean_price'].values.reshape(-1,1))
    return df

def load_data(stock,seq_len):
    amount_of_features=len(stock.columns)
    data=stock.as_matrix()
    sequence_length=seq_len+1
    result=[]

    for index in range(len(data) - sequence_length):
        result.append(data[index:index+sequence_length])

    result=np.array(result)
    row=round(0.9*result.shape[0])
    train=result[:int(row),:]

    x_train=train[:,:-1]
    y_train=train[:,-1][:,-1]
    #print(y_train[:5])

    x_test=result[int(row):,:-1]
    y_test=result[int(row):,-1][:,-1]

    x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],amount_of_features))
    x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],amount_of_features))

    return [x_train,y_train,x_test,y_test]

def build_model(layers):
    d=0.3
    model=Sequential()

    model.add(LSTM(256,input_shape=(layers[1],layers[0]),return_sequences=True))
    model.add(Dropout(d))

    model.add(LSTM(256, input_shape=(layers[1], layers[0]), return_sequences=False))
    model.add(Dropout(d))

    model.add(Dense(32,kernel_initializer='uniform',activation='relu'))
    model.add(Dense(1, kernel_initializer='uniform', activation='linear'))

    start=time.time()
    model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
    print("Compilation time",time.time()-start)
    return model

def denormalize(df,normalize_value):
    df=df['mean_price'].values.reshape(-1,1)
    normalize_value=normalize_value.reshape(-1,1)
    min_max_scaler=preprocessing.MinMaxScaler()
    a=min_max_scaler.fit_transform(df)
    new=min_max_scaler.inverse_transform((normalize_value))
    return new

def model_score(model,X_train,y_train,X_test,y_test):
    train_score=model.evaluate(X_train,y_train,verbose=0)
    print('Train Score: %.5f MSE (%.2f RMSE)' % (train_score[0],math.sqrt(train_score[0])))

    test_score=model.evaluate(X_test,y_test,verbose=0)
    print('Test Score: %.5f MSE (%.2f RMSE)' % (test_score[0], math.sqrt(train_score[0])))
    return train_score[0],test_score[0]

