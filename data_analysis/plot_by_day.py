# -*- coding: utf-8 -*-
import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt

sys.path.append("../module")
from data_manager import DataManager

if __name__ == "__main__":
    datapath = "C:/Users/1615055/DWLab_2020/data"
    os.chdir(datapath)
    data_managers = []

    # open data manager for each data
    for file in glob.glob("*.csv"):
        filename = file
        train_rate = 1.0
        valid_rate = 0.0
        test_rate = 0.0
        data_manager = DataManager(filename, train_rate, valid_rate, test_rate)
        data_managers.append(data_manager)

    #get indices of each day
    lane_inds = []
    for i in range(len(data_managers)):
        day_inds = [] 
        for j in range(7):
            day_inds.append(np.where(data_managers[i].train_day_label == j))
        lane_inds.append(day_inds)

    #plot graph for each day and each lane
    num_samples = 3
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    for i in range(len(data_managers)):
        for j in range(7):
            if len(lane_inds[i][j][0]) >= num_samples:
                fig = plt.figure(i*7+j)
                axes = plt.gca()
                axes.set_xlim([-10,300])
                axes.set_ylim([-10,225])
                samples = np.random.choice(lane_inds[i][j][0], num_samples, replace=False)
                for sample in samples:
                    plt.plot(np.arange(288), data_managers[i].train_input_nan[sample])
                plt.xlabel('time')
                plt.ylabel('traffic')
                fig.suptitle('LANE: '+str(i+1)+" DAY: "+day_dict[j])

    #plot averages of the timeseries of each day
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    for i in range(len(data_managers)):
        fig = plt.figure(i*7+j)
        axes = plt.gca()
        axes.set_xlim([-10,300])
        axes.set_ylim([-10,225])
        for j in range(7):
            temp = data_managers[i].train_input_nan[lane_inds[i][j]].copy()
            temp[temp==-1]=np.nan
            average_timeseries = np.nanmean(temp, axis=0)
            plt.plot(np.arange(288), average_timeseries, label=day_dict[j])            
        plt.xlabel('time')
        plt.ylabel('traffic')
        plt.legend()
        fig.suptitle('LANE: '+str(i+1))