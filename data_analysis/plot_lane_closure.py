# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from datetime import timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    datapath = "C:/Users/1615055/DWLab_2020/data"
    filename = "737257_Lane1.csv"
    data = pd.read_csv(os.path.join(datapath, filename), index_col=[0])
    
    lane_closure_dates = ['2010-01-14', '2010-01-21', '2010-01-25',
                          '2010-02-01', '2010-05-19', '2010-06-07', '2010-06-08', '2010-06-09', '2010-06-10',
                          '2010-06-14', '2010-06-15', '2010-06-16', '2010-09-07', '2010-09-08']
    samples = random.sample(lane_closure_dates, 10)
    
    i=0
    for sample in samples:
        fig = plt.figure(i)
        i = i+1
        axes = plt.gca()
        axes.set_xlim([-10,300])
        axes.set_ylim([-10,225])
        
        # draw graph on the same day as the lane closure date
        sample_datetime = datetime.strptime(sample, "%Y-%m-%d")
        j = 0
        while(True):
            sample_datetime = sample_datetime + timedelta(days=7)
            if sample_datetime.strftime("%Y-%m-%d") in lane_closure_dates:
                continue
            temp_data = data.loc[data.date == sample_datetime.strftime("%Y-%m-%d")]
            temp_array = temp_data.values[0][1:-3]
            plt.plot(np.arange(288), temp_array, color='grey')  
            j = j+1
            if(j>2): break
        
        # draw graph on the same day as the lane closure date
        sample_datetime = datetime.strptime(sample, "%Y-%m-%d")
        j = 0
        while(True):
            sample_datetime = sample_datetime - timedelta(days=7)
            if sample_datetime.strftime("%Y-%m-%d") in lane_closure_dates:
                continue
            if sample_datetime > datetime(2010, 1, 1, 0, 0):
                break
            temp_data = data.loc[data.date == sample_datetime.strftime("%Y-%m-%d")]
            temp_array = temp_data.values[0][1:-3]
            plt.plot(np.arange(288), temp_array, color='grey')  
            j = j+1
            if(j>2): break
        
        # draw graph for sampled lane closure date in red
        temp_data = data.loc[data.date == sample]
        temp_array = temp_data.values[0][1:-3]
        plt.plot(np.arange(288), temp_array, color='red') 
        plt.xlabel('time')
        plt.ylabel('traffic')
        fig.suptitle('DATE: '+sample + " with same day of week data")