# -*- coding: utf-8 -*-
import os
import glob

from module.model import TrafficModel
from module.data_manager import DataManager

if __name__ == "__main__":
    datapath = "./data"
    modelpath = "./model"
    
    #for each data
    for file in glob.glob(os.path.join(datapath, "*.csv")):
        #retrieve data
        filename = file
        train_rate = 0.7
        valid_rate = 0.15
        test_rate = 0.15
        data_manager = DataManager(filename, train_rate, valid_rate, test_rate)
        
        #create model directory
        lane_modelpath = os.path.join(modelpath, filename.split('\\')[1].split('.')[0])
        if not os.path.exists(lane_modelpath):
            os.mkdir(lane_modelpath) 
        
        #day of week classification model
        input_dim = 288
        meta_dim = 290
        output_dim = 7
        hidden_dims = {'CNN': {
                               0: {'num_channel': 30,
                                   'kernel_size': 3},
                               1: {'num_channel': 30,
                                   'kernel_size': 3},
                               2: {'num_channel': 20,
                                   'kernel_size': 3},
                               3: {'num_channel': 20,
                                   'kernel_size': 3},
                               4: {'num_channel': 20,
                                   'kernel_size': 2},
                               5: {'num_channel': 20,
                                   'kernel_size': 2},
                               6: {'num_channel': 20,
                                   'kernel_size': 2},
                               7: {'num_channel': 20,
                                    'kernel_size': 2},
                               8: {'num_channel': 20,
                                   'kernel_size': 2}      
                              },
                       'MLP': [400, 200, 100, 50, 25]      
                      }           
        dropout_rate = 0
        
        #train model with linear interpolated data
        day_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate)
        batch_size = 20
        epochs = 100
        hist = day_model.train_model(data_manager.train_input, data_manager.valid_input, 
                                     data_manager.train_meta, data_manager.valid_meta, 
                                     data_manager.train_day_label, data_manager.valid_day_label, 
                                     batch_size, epochs)
        #evaluate model
        prediction = day_model.predict(data_manager.test_input, data_manager.test_meta)
        test_acc = day_model.compute_acc(prediction, data_manager.test_day_label)
        #save model
        day_model.save_model(os.path.join(lane_modelpath, "day_model_{:.2f}".format(test_acc)), hist)
        
        #train 10 models with -1 as NaN
        day_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate)
        batch_size = 20
        epochs = 100
        hist = day_model.train_model(data_manager.train_input_nan, data_manager.valid_input_nan, 
                                     data_manager.train_meta, data_manager.valid_meta, 
                                     data_manager.train_day_label, data_manager.valid_day_label, 
                                     batch_size, epochs)
        #evaluate model
        prediction = day_model.predict(data_manager.test_input_nan, data_manager.test_meta)
        test_acc = day_model.compute_acc(prediction, data_manager.test_day_label)
        #save model
        day_model.save_model(os.path.join(lane_modelpath, "day_model_NaN_{:.2f}".format(test_acc)), hist)
        
        #week/weekend classification model
        output_dim = 1
        hidden_dims = {'CNN': {0: {'num_channel': 30,
                                   'kernel_size': 3},
                               1: {'num_channel': 30,
                                   'kernel_size': 3},
                               2: {'num_channel': 20,
                                   'kernel_size': 2},
                               3: {'num_channel': 20,
                                   'kernel_size': 2},
                              },
                       'MLP': [200, 100, 50, 25]      
                      }          
        dropout_rate = 0
        
        #train 10 models with linear interpolated data
        week_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate)
        batch_size = 20
        epochs = 100
        hist = week_model.train_model(data_manager.train_input, data_manager.valid_input,
                                      data_manager.train_meta, data_manager.valid_meta, 
                                      data_manager.train_week_label, data_manager.valid_week_label, 
                                      batch_size, epochs)
        #evaluate model
        prediction = week_model.predict(data_manager.test_input, data_manager.test_meta)
        test_acc = week_model.compute_acc(prediction, data_manager.test_week_label)
        #save model
        week_model.save_model(os.path.join(lane_modelpath, "week_model_{:.2f}".format(test_acc)), hist)
            
        #train 10 models with -1 as NaN
        week_model = TrafficModel(input_dim, meta_dim, output_dim, hidden_dims, dropout_rate)
        batch_size = 20
        epochs = 100
        hist = week_model.train_model(data_manager.train_input_nan, data_manager.valid_input_nan,
                                      data_manager.train_meta, data_manager.valid_meta, 
                                      data_manager.train_week_label, data_manager.valid_week_label, 
                                      batch_size, epochs)
        #evaluate model
        prediction = week_model.predict(data_manager.test_input_nan, data_manager.test_meta)
        test_acc = week_model.compute_acc(prediction, data_manager.test_week_label)
        #save model
        week_model.save_model(os.path.join(lane_modelpath, "week_model_NaN_{:.2f}".format(test_acc)), hist)