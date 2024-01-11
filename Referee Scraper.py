import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
# options.add_argument('--user-data-dir=C:/Users/karki/OneDrive/Desktop/User Data');
# options.add_argument('--profile-directory=Profile 7') 
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

driver = webdriver.Chrome(executable_path = "chromedriver.exe", options=options)

wait = WebDriverWait(driver, 20)
action = ActionChains(driver)

driver.get("https://www.bdfutbol.com/en/t/tfra2009-10.html?tab=results")

select = Select(driver.find_element(By.XPATH, "//select[@id='jornada1']"))

select.select_by_visible_text('All')
page_source = driver.page_source


doc = BeautifulSoup(page_source, 'lxml')
# Creating list with all tables
tables = doc.find_all('table')

#  Looking for the table with the classes 'wikitable' and 'sortable'
table = doc.find('table', class_='taula_estil taula_estil-16')

df = pd.DataFrame(columns=['Date', 'Home', 'Away', 'Referee'])

for row in table.tbody.find_all('tr', class_='jornadai'):    
    # Find all data for each column
    columns = row.find_all('td')
    if(columns != []):
        date = columns[0].text.strip()
        home = columns[1].text.strip()
        away = columns[3].text.strip()
        ref = columns[5].text.strip()
        df = df.append({'Date': date,  'Home': home, 
                        'Away': away, 'Referee': ref}, 
                       ignore_index=True)