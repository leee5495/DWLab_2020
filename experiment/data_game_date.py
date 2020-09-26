# -*- coding: utf-8 -*-
import os

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


if __name__ == "__main__":
    url = "https://www.baseball-reference.com/teams/LAD/{}-schedule-scores.shtml"
    browser = webdriver.Chrome(executable_path=r"../chromedriver.exe")
    datapath = '../data/game_dates'
    Path(datapath).mkdir(parents=True, exist_ok=True)
    
    for i in range(2006, 2011):
        browser.get(url.format(i))
        WebDriverWait(browser, 5)
        
        game_dates = []
    
        table=browser.find_element_by_xpath('//*[@id="team_schedule"]/tbody')
        
        for tr in table.find_elements_by_tag_name("tr"):
            if tr.get_attribute("class") == 'thead':
                continue

            date = tr.find_elements_by_tag_name("td")[0].get_attribute("csk")
            home_or_away = tr.find_elements_by_tag_name("td")[3].text
            
            if home_or_away != "@":
                game_dates.append(date)
                
        with open(os.path.join(datapath, str(i)), "w") as fout:
            for date in game_dates:
                fout.write(date + "\n")