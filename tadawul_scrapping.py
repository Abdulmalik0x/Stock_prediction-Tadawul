from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import numpy as np
import seaborn as sns
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from matplotlib import pyplot as plt


def get_data(tadawul_url, from_date, to_date):
    # will fetch the data from historical page
    tadawul_url = 'https://www.tadawul.com.sa/wps/portal/tadawul/market-participants/issuers/issuers-directory' \
                  '/company-details/!ut/p/z1/pdFLb4JAFAXg38KC9ZwZQGh3U7CAPBKqWDqbZtSE0vBaoI3_3il1Y6LYpnd3k' \
                  '-8szr1EkIKIVh6qUg5V18pa7W9i9p4GsRvAYZE_XxngMy9xX9KQASCvI2DMdeiDiRixTRXwEWaJaSAziPhT3g9TGzzjwfp5rajD_peH-bs8bgzH_by4JAiYp8g8ijzXYniyzmDqRJfgyg0mwXfJEUy0WBBR1t3m56Mfw9A_6tAxyJ382te6arntml62x-Wx2XQKUUYp6Zs8zwtU4adVl1zTTgeD9LM!/dz/d5/L0lDUmlTUSEhL3dHa0FKRnNBLzROV3FpQSEhL2Fy/#chart_tab2 '

    os.chdir('/home/abdulmalik0x/SharedFolder/My-projects/stock-analysis/')
    # create a new Firefox session
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(10)
    driver.get(url)
    urls = []

    set_date = driver.find_element_by_xpath('//*[@id="daterangepicker1"]')
    set_date.clear()
    date = "{} - {}".format(from_date, to_date)
    set_date.send_keys(date)  # "2011/06/17 - 2019/07/17"
    driver.find_element_by_xpath('//*[@id="reloadHistoricalData"]').click()
    # driver.find_element_by_xpath('//*[@id="reloadHistoricalData"]').click()

    stock_page = []

    pages = BeautifulSoup(driver.find_element_by_xpath('//*[@id="adjustedPerformanceView_paginate"]/select').text,
                          'lxml')
    pages = pages.findAll('p')[0].text.replace('\n', ',').split(',')[1::]

    for page in pages:
        soup_level1 = None
        soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
        soup_level1 = soup_level1.find('table', {'id': 'adjustedPerformanceView'})
        soup_level1 = soup_level1.find('tbody')
        stock_page.append(soup_level1)
        set_page = Select(driver.find_element_by_xpath('//*[@id="adjustedPerformanceView_paginate"]/select'))
        set_page.select_by_value(page)
        time.sleep(5)

    date = []
    open_price = []
    high = []
    low = []
    close = []
    change = []
    change_prc = []
    traded_amount = []
    traded_price = []
    no_deals = []

    i = 0
    for page in stock_page:
        for tr in page.findAll('tr'):
            date.append(tr.findAll('td')[0].text.strip())
            open_price.append(tr.findAll('td')[1].text.strip())
            high.append(tr.findAll('td')[2].text.strip())
            low.append(tr.findAll('td')[3].text.strip())
            close.append(tr.findAll('td')[4].text.strip())
            change.append(tr.findAll('td')[5].text.strip())
            change_prc.append(tr.findAll('td')[6].text.strip())
            traded_amount.append(tr.findAll('td')[7].text.strip())
            traded_price.append(tr.findAll('td')[8].text.strip())
            no_deals.append(tr.findAll('td')[9].text.strip())

    df = pd.DataFrame(
        {'Date': date, 'Open_price': open_price, 'High': high, 'Low': low, 'Close': close, 'Change': change,
         'Change_prc': change_prc,
         'traded_amount': traded_amount, 'Traded_price': traded_price, 'NO_deals': no_deals}).set_index('Date')
    df.index = pd.to_datetime(df.index)

    df = pd.read_csv('./stocks.csv')
