"""
Auto Login - GUI
By Hyder Pang @ 2023-2-8
"""

import threading
import ctypes
import tkinter as tk
from tkinter import ttk
import time


class GUI:
    def __init__(self, username='Admin', password='123456', retry=3, interval=30,
                 url='http://192.168.12.131/ac_portal/default/pc.html?tabs=pwd',
                 xpath_username='//*[@id=\"password_name\"]',
                 xpath_password='//*[@id=\"password_pwd\"]',
                 xpath_login='//*[@id=\"password_submitBtn\"]',
                 browser='Firefox'):
        # 1. Parameters
        self.username = username
        self.password = password
        self.retry = retry
        self.interval = interval
        self.url = url
        self.xpath_username = xpath_username
        self.xpath_password = xpath_password
        self.xpath_login = xpath_login
        self.browser = browser

        # 2. Layout
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("AutoLogin")

        # 设置窗口固定大小
        self.root.resizable(False, False)

        # 设置多个页面
        self.notebook = ttk.Notebook(self.root)
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)

        # 创建标签和输入框
        # frame 1
        self.username_label = tk.Label(self.frame1, text="Username")
        self.username_entry = tk.Entry(self.frame1, textvariable=tk.StringVar(value=username))
        self.password_label = tk.Label(self.frame1, text="Password")
        self.password_entry = tk.Entry(self.frame1, show="*", textvariable=tk.StringVar(value=password))
        # frame 2
        self.retry_label = tk.Label(self.frame2, text="Retry times")
        self.retry_entry = tk.Entry(self.frame2, textvariable=tk.StringVar(value=retry))
        self.interval_label = tk.Label(self.frame2, text="Listen interval [Sec]")
        self.interval_entry = tk.Entry(self.frame2, textvariable=tk.StringVar(value=interval))
        self.url_label = tk.Label(self.frame2, text="url")
        self.url_entry = tk.Entry(self.frame2, textvariable=tk.StringVar(value=url))
        self.xpath_username_label = tk.Label(self.frame2, text="Xpath of username")
        self.xpath_username_entry = tk.Entry(self.frame2, textvariable=tk.StringVar(value=xpath_username))
        self.xpath_password_label = tk.Label(self.frame2, text="Xpath of password")
        self.xpath_password_entry = tk.Entry(self.frame2, textvariable=tk.StringVar(value=xpath_password))
        self.xpath_login_label = tk.Label(self.frame2, text="Xpath of login")
        self.xpath_login_entry = tk.Entry(self.frame2, textvariable=tk.StringVar(value=xpath_login))

        # 放置标签和输入框
        # self.username_label.grid(row=0, column=0)
        # self.username_entry.grid(row=0, column=1)
        # self.password_label.grid(row=1, column=0)
        # self.password_entry.grid(row=1, column=1)
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()

        self.retry_label.grid(row=0, column=0)
        self.retry_entry.grid(row=0, column=1)
        self.interval_label.grid(row=1, column=0)
        self.interval_entry.grid(row=1, column=1)
        self.url_label.grid(row=2, column=0)
        self.url_entry.grid(row=2, column=1)
        self.xpath_username_label.grid(row=3, column=0)
        self.xpath_username_entry.grid(row=3, column=1)
        self.xpath_password_label.grid(row=4, column=0)
        self.xpath_password_entry.grid(row=4, column=1)
        self.xpath_login_label.grid(row=5, column=0)
        self.xpath_login_entry.grid(row=5, column=1)

        # 放置复选框
        self.browser_label = tk.Label(self.frame2, text="Browser (Exists in $PATH)")
        self.browser_cmb = ttk.Combobox(self.frame2)
        self.browser_cmb['value'] = ('Firefox', 'Chrome', 'Edge')
        self.browser_cmb.current(0)
        self.browser_label.grid(row=6, column=0)
        self.browser_cmb.grid(row=6, column=1)

        # 放置页面
        self.notebook.add(self.frame1, text='Login')
        self.notebook.add(self.frame2, text='Setting')
        self.notebook.grid(row=0, column=0)

        # 创建并放置按键
        self.button_pressed = False
        self.button_text = tk.StringVar()
        self.button_text.set('Press to Activate')
        self.button = tk.Button(self.root, textvariable=self.button_text, command=self.__button_cb)
        self.button.grid(row=7, column=0)
        self.button_pressed_cb = None
        self.button_released_cb = None

    def run(self):
        self.root.mainloop()

    def __button_cb(self):
        if self.button_pressed:
            self.button_pressed = False
            self.button_text.set('Press to Activate')
            self.button_released_cb()
        else:
            self.button_pressed = True
            self.button_text.set('Press to Deactivate')
            self.button_pressed_cb()

    def set_button_callback(self, pressed_func, released_func):
        self.button_pressed_cb = pressed_func
        self.button_released_cb = released_func
        self.button.grid(row=8, columnspan=2)

    def get_attr(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.retry = int(self.retry_entry.get())
        self.interval = int(self.interval_entry.get())
        self.url = self.url_entry.get()
        self.xpath_username = self.xpath_username_entry.get()
        self.xpath_password = self.xpath_password_entry.get()
        self.xpath_login = self.xpath_login_entry.get()
        self.browser = self.browser_cmb.get()

        attr = {
            'username': self.username,
            'password': self.password,
            'retry': self.retry,
            'interval': self.interval,
            'url': self.url,
            'xpath_username': self.xpath_username,
            'xpath_password': self.xpath_password,
            'xpath_login': self.xpath_login,
            'browser': self.browser,
        }
        return attr


if __name__ == '__main__':

    class myThread:

        def __init__(self):
            self.thread = None

        def start(self):
            self.thread = threading.Thread(target=self.test_func)
            global thread_stop
            thread_stop = False
            self.thread.start()

        def stop(self):
            global thread_stop
            thread_stop = True
            self.thread.join()

        def test_func(self):
            while True:
                global thread_stop
                if thread_stop:
                    break
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                time.sleep(1)


    t1 = myThread()

    gui = GUI()
    gui.set_button_callback(t1.start, t1.stop)
    gui.run()
