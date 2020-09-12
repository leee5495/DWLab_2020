# DWLab_2020
Experimentation code for Pattern Classification Model based on Attention Mechanism and CNN for Analysis of Traffic Data including Missing Values

### data.py
scrapes [Caltrans PeMS](http://pems.dot.ca.gov/) traffic data 
- `station_id`:  id of the station in interest
- `start_time`:  start date in the format 'YYYY/MM/DD'
- `end_time`:  end date in the format 'YYYY/MM/DD'
- `num_lane`:  number of lanes in the station
- `destpath`:  directory path to save the scraped data
- `browser`:  path to the selenium browser

### preprocess.py
preprocesses the scraped data and makes a timeseries data
- `srcpath`:  directory path to the original data
- `destpath`:  directory path to save the preprocessed data

### train.py
trains the timeseries traffic data using the pattern classification model
- `datapath`:  directory path to the preprocessed data
- `modelpath`:  directory path to save the trained models
