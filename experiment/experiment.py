# -*- coding: utf-8 -*-
import os
import sys
import glob

import pandas as pd

sys.path.append("..")
from module.model import TrafficModel
from module.data_manager import DataManager


if __name__ == "__main__":
    datapath = "../data"
    modelpath = "../model"
    data_managers = []
    
    #for each data
    for file in glob.glob(os.path.join(datapath, "*.csv")):
        #retrieve data
        filename = file
        train_rate = 0.75
        valid_rate = 0.1
        test_rate = 0.15
        data_manager = DataManager(filename, train_rate, valid_rate, test_rate)
        data_managers.append(data_manager)
        
    accuracies = pd.DataFrame(columns = ['year', 'attention', 'preprocessing', 'avg_accuracy'])
    
    # hyperparameters
    input_dim = 288
    meta_dim = 290
    output_dim = 2
    hidden_dims = {'CNN': {
                            0: {
                                'num_channel': 30,
                                'kernel_size': 2},
                            1: {
                                'num_channel': 30,
                                'kernel_size': 2},
                            2: {
                                'num_channel': 20,
                                'kernel_size': 2},
                            3: {
                                'num_channel': 20,
                                'kernel_size': 3},
                            4: {
                                'num_channel': 20,
                                'kernel_size': 3},
                            },
                   'MLP': [400, 200, 100, 50, 25]} 
    dropout_rate = 0.2    
    batch_size = 20
    epochs = 100
    
    for idx, year in enumerate(range(2006, 2011)):
        year_destpath = os.path.join(modelpath, "year_"+str(year))
        if not os.path.exists(year_destpath):
            os.mkdir(year_destpath)
         
        """ATTENTION MODEL"""            
        #train linear interpolated data
        temp_acc = []
        for j in range(3):
            game_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate, use_att=True)
            hist = game_model.train_model(data_managers[idx].train_input, data_managers[idx].valid_input, 
                                          data_managers[idx].train_meta, data_managers[idx].valid_meta, 
                                          data_managers[idx].train_day_label, data_managers[idx].valid_day_label, 
                                          batch_size, epochs)
            #evaluate model
            prediction = game_model.predict(data_managers[idx].test_input, data_managers[idx].test_meta)
            test_acc = game_model.compute_acc(prediction, data_managers[idx].test_day_label)
            #save model
            game_model.save_model(os.path.join(year_destpath, "game_model_att_"+str(j+1)+"_"+"{:.3f}".format(test_acc)))
            temp_acc.append(test_acc)
            
        accuracies = accuracies.append({'year': year, 'attention': 'Y', 'preprocessing': 'linear interpolated', 'avg_accuracy': sum(temp_acc)/3}, ignore_index=True)
        
        #train unpreprocessed data
        temp_acc = []
        for j in range(3):
            game_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate, use_att=True)
            
            hist = game_model.train_model(data_managers[idx].train_input_nan, data_managers[idx].valid_input_nan, 
                                          data_managers[idx].train_meta, data_managers[idx].valid_meta, 
                                          data_managers[idx].train_day_label, data_managers[idx].valid_day_label, 
                                          batch_size, epochs)
            #evaluate model
            prediction = game_model.predict(data_managers[idx].test_input_nan, data_managers[idx].test_meta)
            test_acc = game_model.compute_acc(prediction, data_managers[idx].test_day_label)
            #save model
            game_model.save_model(os.path.join(year_destpath, "game_model_att_NaN_"+str(j+1)+"_"+"{:.3f}".format(test_acc)))
            temp_acc.append(test_acc)
        
        accuracies = accuracies.append({'year': year, 'attention': 'Y', 'preprocessing': 'NaN', 'avg_accuracy': sum(temp_acc)/3}, ignore_index=True)    
    
        """NO ATTENTION MODEL"""            
        #train linear interpolated data
        temp_acc = []
        for j in range(3):
            game_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate, use_att=False)
            
            hist = game_model.train_model(data_managers[idx].train_input, data_managers[idx].valid_input, 
                                          data_managers[idx].train_meta, data_managers[idx].valid_meta, 
                                          data_managers[idx].train_day_label, data_managers[idx].valid_day_label, 
                                          batch_size, epochs)
            #evaluate model
            prediction = game_model.predict(data_managers[idx].test_input, data_managers[idx].test_meta)
            test_acc = game_model.compute_acc(prediction, data_managers[idx].test_day_label)
            #save model
            game_model.save_model(os.path.join(year_destpath, "game_model_no_att_"+str(j+1)+"_"+"{:.3f}".format(test_acc)))
            temp_acc.append(test_acc)
            
        accuracies = accuracies.append({'year': year, 'attention': 'N', 'preprocessing': 'linear interpolated', 'avg_accuracy': sum(temp_acc)/3}, ignore_index=True)
        
        #train unpreprocessed data
        temp_acc = []
        for j in range(3):
            game_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate, use_att=False)
            
            hist = game_model.train_model(data_managers[idx].train_input_nan, data_managers[idx].valid_input_nan, 
                                          data_managers[idx].train_meta, data_managers[idx].valid_meta, 
                                          data_managers[idx].train_day_label, data_managers[idx].valid_day_label, 
                                          batch_size, epochs)
            #evaluate model
            prediction = game_model.predict(data_managers[idx].test_input_nan, data_managers[idx].test_meta)
            test_acc = game_model.compute_acc(prediction, data_managers[idx].test_day_label)
            #save model
            game_model.save_model(os.path.join(year_destpath, "game_model_no_att_NaN_"+str(j+1)+"_"+"{:.3f}".format(test_acc)))
            temp_acc.append(test_acc)
        
        accuracies = accuracies.append({'year': year, 'attention': 'N', 'preprocessing': 'NaN', 'avg_accuracy': sum(temp_acc)/3}, ignore_index=True)
    
    accuracies.to_csv(os.path.join(modelpath, "accuracies.csv"))