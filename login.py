"""
Auto Login - Web
By Hyder Pang @ 2023-2-8
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import sys


def isConnected():
    try:
        html = requests.get("https://www.bilibili.com/", timeout=2)
        return 1
    except:
        return 0


def login(username, password, retry, url, xpath_username, xpath_password, xpath_login, browser):
    for i in range(retry):
        # 1. Open browser.
        if browser == 'Firefox':
            driver = webdriver.Firefox()
        elif browser == 'Chrome':
            driver = webdriver.Chrome()
        elif browser == 'Edge':
            driver = webdriver.Edge()
        driver.get(url)
        time.sleep(0.2)

        # 2. Input username.
        # pasted from firefox-查看器-element右键复制XPATH
        el = driver.find_element(By.XPATH, xpath_username)
        el.send_keys(username)
        time.sleep(0.2)

        # 3. Input password.
        el = driver.find_element(By.XPATH, xpath_password)
        el.send_keys(password)
        time.sleep(0.2)

        # 4. Click login button.
        el = driver.find_element(By.XPATH, xpath_login)
        el.click()
        time.sleep(0.2)

        driver.quit()
        if isConnected():
            return True
    return False


def get_timestamp():
    t = time.localtime()
    stamp = '%4d-%2d-%2d %02d:%02d:%02d' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return stamp


def try_login(username, password, retry=1,
              url='http://192.168.12.131/ac_portal/default/pc.html?tabs=pwd',
              xpath_username='//*[@id=\"password_name\"]',
              xpath_password='//*[@id=\"password_pwd\"]',
              xpath_login='//*[@id=\"password_submitBtn\"]',
              browser='Firefox',
              ):
    connected_flag = isConnected()
    if not connected_flag:
        print(get_timestamp() + '#Connection lost. Reconnecting...')
        connected_flag = login(username, password, retry, url, xpath_username, xpath_password, xpath_login, browser)
    if not connected_flag:
        print('Max retry number exceeded and still not connected, the program will try again later.')
        print('Please check cable, account, etc.')
    else:
        print(get_timestamp() + '#Connected. ')


def auto_login(username, password, retry=3, interval=10):
    try_login(username, password, retry)
    thread_cnt = 0
    while True:
        thread_cnt += 1
        if thread_cnt > interval:
            thread_cnt = 0
            try_login(username, password, retry)
        time.sleep(1)


if __name__ == '__main__':
    Username = 'admin'
    Password = '12345'
    auto_login(Username, Password)
