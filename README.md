# DWLab 2020
Experimentation code for Pattern Classification Model based on Attention Mechanism and CNN for Analysis of Traffic Data including Missing Values

Paper: [Pattern Classification based on Attention Mechanism and CNN for Sensor Stream Data including Missing Values](https://github.com/leee5495/DWLab_2020/blob/master/misc/KDBC_lej.pdf)
<br>
<br>

![image](https://github.com/leee5495/DWLab_2020/blob/master/misc/%EB%8F%84%ED%98%95.png)


### data.py
scrapes [Caltrans PeMS](http://pems.dot.ca.gov/) traffic data 
``` python
# run this command to scrape traffic data to destpath
$ python data.py
```
- `station_id`:  id of the station in interest
- `start_time`:  start date in the format 'YYYY/MM/DD'
- `end_time`:  end date in the format 'YYYY/MM/DD'
- `num_lane`:  number of lanes in the station
- `destpath`:  directory path to save the scraped data
- `browser`:  path to the selenium browser

### preprocess.py
preprocesses the scraped data and makes a timeseries data
``` python
# run this command to preprocess data
$ python preprocess.py
```
- `srcpath`:  directory path to the original data
- `destpath`:  directory path to save the preprocessed data

### train.py
trains the timeseries traffic data using the pattern classification model
``` python
# run this command to train the traffic data pattern classification model
$ python train.py
```
- `datapath`:  directory path to the preprocessed data
- `modelpath`:  directory path to save the trained models
- hyperparameters
  - `hidden_dims` = hidden dimensions for each CNN and MLP layer given as dictionary
  - `dropout_rate` = dropout rate
  - `pooling_size` = pooling size for each CNN pooling layer
  - `stride_size` = stride size for each CNN layer
  - `pooling_method` = "avg" or "max"
