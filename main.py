"""
Auto Login
By Hyder Pang @ 2023-2-8
"""

from gui import GUI
from login import try_login
from encoding_io import base64_io

import time
import os
import threading


username = 'Admin'
password = '12345'
retry = 3
interval = 30
url = 'http://192.168.12.131/ac_portal/default/pc.html?tabs=pwd'
xpath_username = '//*[@id=\"password_name\"]'
xpath_password = '//*[@id=\"password_pwd\"]'
xpath_login = '//*[@id=\"password_submitBtn\"]'
browser = 'Firefox'

local_store_file = 'autologin.log'

# Read stored parameters.
io = base64_io()
files = os.listdir()
if local_store_file in files:
    local_store_file_path = os.getcwd() + os.sep + local_store_file
    local_strs = io.read_from_file(local_store_file_path)
    if len(local_strs) == 9:
        username = local_strs[0]
        password = local_strs[1]
        retry = int(local_strs[2])
        interval = int(local_strs[3])
        url = local_strs[4]
        xpath_username = local_strs[5]
        xpath_password = local_strs[6]
        xpath_login = local_strs[7]
        browser = local_strs[8]
    else:
        os.remove(local_store_file_path)
        raise IOError('Wrong format for %s, %d of %d, deleted!' % (local_store_file, len(local_strs), 9))

# Auto login function
global thread_stop
thread_stop = False


# GUI
class myThread:
    def __init__(self, _gui):
        self.thread = None
        self.gui = _gui
        self.username = _gui.username
        self.password = _gui.password
        self.retry = _gui.retry
        self.interval = _gui.interval
        self.url = _gui.url
        self.xpath_username = _gui.xpath_username
        self.xpath_password = _gui.xpath_password
        self.xpath_login = _gui.xpath_login
        self.browser = _gui.browser

    def start(self):
        # Update username, etc.
        gui_attr = self.gui.get_attr()
        self.username = gui_attr['username']
        self.password = gui_attr['password']
        self.retry = gui_attr['retry']
        self.interval = gui_attr['interval']
        self.url = gui_attr['url']
        self.xpath_username = gui_attr['xpath_username']
        self.xpath_password = gui_attr['xpath_password']
        self.xpath_login = gui_attr['xpath_login']
        self.browser = gui_attr['browser']

        # Write log.
        io.write_to_file([self.username, self.password, str(self.retry), str(self.interval),
                          self.url, self.xpath_username, self.xpath_password,
                          self.xpath_login, self.browser], local_store_file)
        # Start thread.
        self.thread = threading.Thread(target=self.auto_login)
        global thread_stop
        thread_stop = False
        self.thread.start()

    def stop(self):
        global thread_stop
        thread_stop = True
        self.thread.join()

    def auto_login(self, response_time=0.1):
        try_login(self.username, self.password, self.retry, self.url,
                  self.xpath_username, self.xpath_password, self.xpath_login, self.browser)

        thread_cnt = 0
        while True:
            global thread_stop
            if thread_stop:
                print("Deactivated.")
                break

            thread_cnt += 1
            if thread_cnt > self.interval * 1.0 / response_time:
                thread_cnt = 0
                try_login(self.username, self.password, self.retry, self.url,
                          self.xpath_username, self.xpath_password, self.xpath_login, self.browser)
            time.sleep(response_time)


gui = GUI(username, password, retry, interval, url, xpath_username, xpath_password, xpath_login, browser)
t1 = myThread(gui)
gui.set_button_callback(t1.start, t1.stop)
gui.run()
