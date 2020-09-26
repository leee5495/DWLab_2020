# -*- coding: utf-8 -*-
import os
import glob
from datetime import timedelta

import pandas as pd

class Preprocess:
    def __init__(self, srcpath, destpath):
        self.srcpath = srcpath
        self.destpath = destpath
        self.preprocess()
        
    def preprocess(self):
        for station in os.listdir(self.srcpath):
            station_datapath = os.path.join(self.srcpath, station)
            for lane in os.listdir(station_datapath):
                whole_data = pd.DataFrame(columns=['5 Minutes', 'Flow (Veh/5 Minutes)', '# Lane Points', '% Observed'])
                lane_datapath = os.path.join(station_datapath, lane)
                # for each file in the lane directory
                for file in glob.glob(os.path.join(lane_datapath, "*.txt")):
                    # read data
                    data = pd.read_csv(file, delimiter="\t")
                    data = data.astype(str)
                    # replace NaN data with -1
                    for _, row in data.iterrows():
                        if(float(row[-1].replace(',','')) == 0):
                            row[1] = -1
                    # concatenate data
                    data.columns = ['5 Minutes', 'Flow (Veh/5 Minutes)', '# Lane Points', '% Observed']
                    whole_data = whole_data.append(data, ignore_index=True)
                # make model input
                input_data = self.make_input(whole_data)
                input_data = self.add_game_info(input_data, station)
                # write input data to the destpath
                input_data.to_csv(os.path.join(self.destpath, station+"_"+lane+".csv"), sep=',')

    def make_input(self, data):
        #format datetime
        data['5 Minutes'] = pd.to_datetime(data['5 Minutes'])
        data.sort_values(by=['5 Minutes'], inplace=True)
        data.reset_index(drop=True, inplace=True)
        
        #create input_data dataframe
        columns = ['date']
        for i in range(288):
            columns.append(i+1)
        columns.extend(['day', 'week/weekend', 'num_nan'])
        input_data = pd.DataFrame(columns=columns)
        
        day_to_week = {0: 0, 1:0, 2:0, 3:0, 4:0, 5:1, 6:1}
        cur_ind = 0
        num_nan = 0
        
        #iterate over data rows
        while(True):
            new_data = {}
            cur_date = data.iloc[cur_ind]['5 Minutes']
            new_data['date'] = cur_date
            num_nan = 0
            for i in range(288):
                if(cur_ind==0 or data.iloc[cur_ind]['5 Minutes']-data.iloc[cur_ind-1]['5 Minutes'] == timedelta(0,300)):                
                    new_data[i+1] = data.iloc[cur_ind]['Flow (Veh/5 Minutes)']
                    if(new_data[i+1] == -1):
                        num_nan = num_nan+1
                    cur_ind = cur_ind+1
                else:
                    new_data[i+1] = -1
                    num_nan = num_nan+1
                    data.at[cur_ind-1, '5 Minutes'] = data.at[cur_ind-1, '5 Minutes'] + timedelta(0, 300)
            new_data['day'] = cur_date.weekday()
            new_data['week/weekend'] = day_to_week[cur_date.weekday()]
            new_data['num_nan'] = num_nan
            input_data = input_data.append(new_data, ignore_index=True)
            if(cur_ind >= data.shape[0]):
                break
        return input_data
    
    def add_game_info(self, data, year):
        # replace day of the week label to game label (binary label for game/no game)
        with open(os.path.join(self.srcpath, "game_dates", str(year)), "r") as fin:
            game_dates = [line.strip() for line in fin]
        data.rename(columns={'day': 'game'}, inplace=True)
        data['game'] = 0
        for date in game_dates:
            data.loc[data['date'] == date, 'game'] = 1
        return data        
    

if __name__ == "__main__":
    # test parameters
    srcpath = "../data"
    destpath = "../data"
    Preprocess(srcpath, destpath)