import json
import sys
import time
import urllib.parse

import lxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LATEST_INFO = '#app > div > div > ul > a:nth-child(1) > li > section > h1'
last_modified = ''


with open('config/config.json', 'r') as f:
    conf = json.load(f)
    URL = conf.get('url')
    WEBHOOK_URL = conf.get('webhook')
    CHECK_INTERBAL = int(conf.get('check_interbal'))

if not URL or not WEBHOOK_URL:
    print('url is None')
    exit(1)

if not CHECK_INTERBAL:
    CHECK_INTERBAL = 300

op = Options()
op.add_argument('--disable-gpu');
op.add_argument('--disable-extensions');
op.add_argument('--proxy-server="direct://"');
op.add_argument('--proxy-bypass-list=*');
op.add_argument('--start-maximized');
op.add_argument('--headless');

while True:
    driver = webdriver.Chrome(options=op)
    driver.get(URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, LATEST_INFO))
    )

    entory = BeautifulSoup(driver.page_source, 'lxml').find('a')
    title = entory.h1.get_text()
    timestamp = entory.span.get_text()
    shousai_url = urllib.parse.urljoin(URL, entory.get('href'))
    print(f'{title}: {timestamp}')
    if last_modified:
        if last_modified != timestamp:
            res = post_webhook(title, timestamp, shousai_url)
            if not res in [200, 201, 204]:
                print('post fail')
    last_modified = timestamp
    driver.close()
    time.sleep(CHECK_INTERBAL)

def post_webhook(title, timestamp, shousai_url):
    payload = {
        'content': 'UPDATE!! '+timestamp,
        'embeds': [{
            'author': {
                'name': '青羽美咲',
                'icon_url': 'https://pbs.twimg.com/profile_images/1128990062274727936/Ij_DjSNo_400x400.png'
            },
            'title': title,
            'description': 'Check [detail]('+shousai_url+')\nBy the way, [PLEASE FOLLOW ME.](https://twitter.com/imasml_theater)',
            'color': 7656389
        }]
    }
    return requests.post(WEBHOOK_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))