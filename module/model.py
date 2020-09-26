# -*- coding: utf-8 -*-
import pickle

import numpy as np
from keras.models import Model
from keras.models import load_model
from keras.layers import Input, Reshape, Dropout, Dense, Conv2D, Flatten, MaxPooling2D, AveragePooling2D, Concatenate, Multiply

class TrafficModel:
    def __init__(self, input_dim, meta_dim, output_dim, hidden_dims, dropout_rate, use_att=True, pooling_size=2, stride_size=2, pooling_method="max", import_model=False, modelname=''):
        self.input_dim = input_dim
        self.meta_dim = meta_dim
        self.output_dim = output_dim
        self.hidden_dims = hidden_dims
        self.dropout_rate = dropout_rate
        self.use_att = use_att
        self.pooling_size = pooling_size
        self.stride_size = stride_size
        self.pooling_method = pooling_method
        if import_model:
            self.model = load_model(modelname)
        else:
            self.model = self.create_model()
        
    def create_model(self):
        #input layers
        input_layer = Input(shape=(self.input_dim,))
        if self.use_att:
            meta_input_layer = Input(shape=(self.meta_dim,))
        
        #process attention
        if self.use_att:
            state = Concatenate()([input_layer, meta_input_layer])
            p0 = Dense(self.input_dim, activation='relu')(state)
            p0 = Dense(self.input_dim, activation='sigmoid')(p0)
            hidden = Multiply()([input_layer, p0])
        else:
            hidden = input_layer
        
        #CNN
        hidden = Reshape((self.input_dim,1,1))(hidden)
        for layer in range(len(self.hidden_dims['CNN'])):
            hidden = Conv2D(self.hidden_dims['CNN'][layer]['num_channel'], 
                            (self.hidden_dims['CNN'][layer]['kernel_size'],1),
                            strides = (self.stride_size, 1),
                            activation='relu', padding='same')(hidden)
            hidden = Dropout(self.dropout_rate)(hidden)
            if self.pooling_method=="max":
                hidden = MaxPooling2D((self.pooling_size,1), padding='same')(hidden)
            elif self.pooling_method=="avg":
                hidden = AveragePooling2D((self.pooling_size,1), padding='same')(hidden)
        
        #MLP
        hidden = Flatten()(hidden)
        for layer in range(len(self.hidden_dims['MLP'])):
            hidden = Dense(self.hidden_dims['MLP'][layer], activation = 'relu')(hidden)
            hidden = Dropout(self.dropout_rate)(hidden)
            
        #output
        output = Dense(self.output_dim, activation="sigmoid")(hidden)
        
        #create model and return the model
        model = Model(inputs=[input_layer, meta_input_layer], outputs=output)
        if(self.output_dim == 1):
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        else:
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def train_model(self, train_input_data, valid_input_data, train_meta_data, valid_meta_data, train_label, valid_label, batch_size, epochs):
        #create categorical one hot array if output_dim > 1
        if(self.output_dim > 1):
            temp = np.zeros((train_label.shape[0], self.output_dim))
            temp[np.arange(train_label.shape[0]),train_label] = 1
            train_label = temp

            temp = np.zeros((valid_label.shape[0], self.output_dim))
            temp[np.arange(valid_label.shape[0]), valid_label] = 1
            valid_label = temp
            
        history = self.model.fit([train_input_data, train_meta_data], train_label,
                        batch_size=batch_size, epochs=epochs,
                        verbose=1, validation_data=[[valid_input_data, valid_meta_data], valid_label])
        return history
    
    def predict(self, test_input_data, test_meta_data):
        prediction = self.model.predict([test_input_data, test_meta_data])
        return prediction
    
    def compute_acc(self, prediction, label):
        #if a binary prediction problem
        if(self.output_dim == 1):
            predicted_label = [0 if i<0.5 else 1 for i in prediction]
        #else if a categorical classification problem
        else:
            predicted_label = prediction.argmax(axis=-1)
        test_accuracy = sum([1 if predicted_label[i]==label[i] else 0 for i in range(len(predicted_label))])/len(predicted_label)
        return test_accuracy
        
    def save_model(self, modelname, hist=None):
        #self.model.save(modelname+".h5")
        with open(modelname, "w") as fp:
            fp.write('')
        if hist is not None:
            with open(modelname+"_hist", "wb") as fp:
                pickle.dump(hist, fp)