# -*- coding: utf-8 -*-
import pickle
import random

import numpy as np
import pandas as pd

class DataManager:
    def __init__(self, filename, train_rate=0.8, valid_rate=0.1, test_rate=0.1, load_data=False):
        self.filename = filename
        self.train_rate = train_rate
        self.valid_rate = valid_rate
        self.test_rate = test_rate
        if load_data:
            self.load_data()
        else:
            self.divide_data()
        
    def divide_data(self):
        data = pd.read_csv(self.filename, index_col=[0])
        #convert -1 to NaN
        data[data == -1] = np.nan
        
        #drop data where all are NaN
        columns = []
        for i in range(288):
            columns.append(str(i+1))
        data = data.dropna(axis=0, subset=columns, how='all')
        
        #create meta input (whether nan for each cell, 0/1 for with nan or not)
        meta_data = pd.isnull(data).values[:,1:-3]*1
        has_nan_ind = np.where(np.sum(meta_data, axis=1)>0,1,0)
        has_nan = np.zeros((len(has_nan_ind),2))
        has_nan[np.arange(len(has_nan_ind)), has_nan_ind] = 1
        meta_data = np.concatenate([meta_data, has_nan], axis=1)
        
        #linear interpolate
        interpolate_data = data.copy()
        interpolate_data.iloc[:,1:-3] = interpolate_data.iloc[:,1:-3].interpolate(axis=1, limit_direction="both")
        
        #reconvert NaN to -1 in data
        data = data.fillna(-1)
        
        #select train/valid/test set
        inds = []
        for i in range(data.shape[0]):
            inds.append(i)
        random.shuffle(inds)
            
        train_ind = inds[:int(len(inds)*self.train_rate)]
        valid_ind = inds[int(len(inds)*self.train_rate):-int(len(inds)*self.test_rate)]
        test_ind = inds[-int(len(inds)*self.test_rate):]
        
        self.train_input = interpolate_data.iloc[train_ind,1:-3].values
        self.train_input_nan = data.iloc[train_ind, 1:-3].values
        self.train_meta = meta_data[train_ind]
        self.train_day_label = data.iloc[train_ind, -3].values
        self.train_week_label = data.iloc[train_ind, -2].values
        
        self.valid_input = interpolate_data.iloc[valid_ind,1:-3].values
        self.valid_input_nan = data.iloc[valid_ind, 1:-3].values
        self.valid_meta = meta_data[valid_ind]
        self.valid_day_label = data.iloc[valid_ind, -3].values
        self.valid_week_label = data.iloc[valid_ind, -2].values
        
        self.test_input = interpolate_data.iloc[test_ind,1:-3].values
        self.test_input_nan = data.iloc[test_ind, 1:-3].values
        self.test_meta = meta_data[test_ind]
        self.test_day_label = data.iloc[test_ind, -3].values
        self.test_week_label = data.iloc[test_ind, -2].values
        
    def save_data(self, dataname):
        data = {
                'train_input': self.train_input,
                'train_input_nan': self.train_input_nan,
                'train_meta': self.train_meta,
                'train_day_label': self.train_day_label,
                'train_week_label': self.train_week_label,
                
                'valid_input': self.valid_input,
                'valid_input_nan': self.valid_input_nan,
                'valid_meta': self.valid_meta,
                'valid_day_label': self.valid_day_label,
                'valid_week_label': self.valid_week_label,
                
                'test_input': self.test_input,
                'test_input_nan': self.test_input_nan,
                'test_meta': self.test_meta,
                'test_day_label': self.test_day_label,
                'test_week_label': self.test_week_label
                }
        with open(dataname, "wb") as fp:
            pickle.dump(data, fp)
            
    def load_data(self):
        with open(self.filename, "rb") as fp:
            data = pickle.load(fp)

        self.train_input = data['train_input']
        self.train_input_nan = data['train_input_nan']
        self.train_meta = data['train_meta']
        self.train_day_label = data['train_day_label']
        self.train_week_label = data['train_week_label']
        
        self.valid_input = data['valid_input']
        self.valid_input_nan = data['valid_input_nan']
        self.valid_meta = data['valid_meta']
        self.valid_day_label = data['valid_day_label']
        self.valid_week_label = data['valid_week_label']
        
        self.test_input = data['test_input']
        self.test_input_nan = data['test_input_nan']
        self.test_meta = data['test_meta']
        self.test_day_label = data['test_day_label']
        self.test_week_label = data['test_week_label']