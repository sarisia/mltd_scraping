import json
import sys

import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LATEST_INFO = '#app > div > div > ul > a:nth-child(1) > li > section > h1'

with open('config/config.json', 'r') as f:
    conf = json.load(f)
    URL = conf.get("url")

if not URL:
    print("url is None")
    exit(1)

op = Options()
op.add_argument("--disable-gpu");
op.add_argument("--disable-extensions");
op.add_argument("--proxy-server='direct://'");
op.add_argument("--proxy-bypass-list=*");
op.add_argument("--start-maximized");
op.add_argument("--headless");
driver = webdriver.Chrome(options=op)

driver.get(URL)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, LATEST_INFO))
)

soup = BeautifulSoup(driver.page_source, 'lxml')

text = soup.find_all("h1")
for title in text:
    print(title.text)

driver.close()