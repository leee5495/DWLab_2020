# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# path to the selenium browser
browser = webdriver.Chrome(executable_path=r"C:\\Users\\1615055\\DWLab_2020\\chromedriver.exe")

class ScrapePeMS:
    def __init__(self, station_id, start_time, end_time, num_lane, destpath):
        self.station_id = station_id
        self.start_time = start_time
        self.end_time = end_time
        self.num_lane = num_lane
        self.destpath = destpath
        self.createDir()
        self.downloadFile()

    def createDir(self):
        # create directories
        # for each lane
        for i in range(self.num_lane):
            new_dir = os.path.join(self.destpath, "Lane"+str(i+1))
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
        #for all aggregates
        new_dir = os.path.join(self.destpath, "Agg")
        if not os.path.exists(new_dir):
                os.mkdir(new_dir) 
                
    def downloadFile(self):
        file_url = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=text&station_id={}&s_time_id={}&e_time_id={}&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&gn=5min&{}'
        time_diff = 32400
        end_time = time.mktime(datetime(int(self.end_time.split('/')[0]), int(self.end_time.split('/')[1]), int(self.end_time.split('/')[2]), 23, 55).timetuple()) + time_diff
        
        #for each lane download data
        for i in range(self.num_lane):
            temp_start_time = time.mktime(datetime(int(self.start_time.split('/')[0]), int(self.start_time.split('/')[1]), int(self.start_time.split('/')[2]), 0, 0).timetuple()) + time_diff
            temp_end_time = temp_start_time + 604500
            
            while(True):
                #file = requests.get(file_url.format(self.station_id, temp_start_time, temp_end_time, "lane"+str(i+1)+"=on"))
                browser.get(file_url.format(self.station_id, temp_start_time, temp_end_time, "lane"+str(i+1)+"=on"))
                WebDriverWait(browser, 5)
                filename = datetime.utcfromtimestamp(temp_start_time).strftime('%Y%m%d') + '-' + datetime.utcfromtimestamp(temp_end_time-time_diff).strftime('%m%d')
                with open(os.path.join(self.destpath, 'Lane'+str(i+1)+'/'+filename+".txt"), 'w') as f:
                    #f.write(file.content)
                    f.write(browser.page_source.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace('</pre></body></html>', ''))
                temp_start_time += 604800
                temp_end_time = min(temp_end_time+604800, end_time)
                if(temp_start_time >= end_time):
                    break
        
        #for all aggregates download data
        temp_start_time = time.mktime(datetime(int(self.start_time.split('/')[0]), int(self.start_time.split('/')[1]), int(self.start_time.split('/')[2]), 0, 0).timetuple()) + time_diff
        temp_end_time = temp_start_time + 604500
        
        while(True):
            #file = requests.get(file_url.format(self.station_id, temp_start_time, temp_end_time, "agg=on"))
            browser.get(file_url.format(self.station_id, temp_start_time, temp_end_time, "agg=on"))
            WebDriverWait(browser, 5)
            filename = datetime.utcfromtimestamp(temp_start_time).strftime('%Y%m%d') + '-' + datetime.utcfromtimestamp(temp_end_time-time_diff).strftime('%m%d')
            with open(os.path.join(self.destpath, 'Agg/'+filename+".txt"), 'w') as f:
                #f.write(file.content)
                f.write(browser.page_source.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace('</pre></body></html>', ''))
            temp_start_time += 604800
            temp_end_time = min(temp_end_time+604800, end_time)
            if(temp_start_time >= end_time):
                break

if __name__ == "__main__":
    # test parameters         
    station_id = 717014
    start_time = '2010/01/01'
    end_time = '2010/02/28'
    num_lane = 4
    destpath = os.path.join('C:\\Users\\1615055\\DWLab_2020\\data', str(station_id))
    
    browser.get('http://pems.dot.ca.gov/')
    # must login first to run the following code
    # module = ScrapePeMS(station_id, start_time, end_time, num_lane, destpath)  