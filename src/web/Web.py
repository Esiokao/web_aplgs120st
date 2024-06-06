from selenium import webdriver

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(parent_dir)

from web.login import login
from web.set_prop import set_prop
from web.check import check


class Web:

    def __init__(self, service, logger, telnet_instance, target_url,
                 timeout_time, implicitly_wait_time):
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(implicitly_wait_time)
        self.logger = logger
        self.target_url = target_url
        self.timeout_time = timeout_time
        self.telnet_instance = telnet_instance

    def init_driver(self, service, implicitly_wait_time):
        if self.driver:
            self.driver.quit()
            self.driver = None
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(implicitly_wait_time)

    def login(self, username, page_title):

        login(self.driver, self.target_url, page_title, username, self.logger,
              self.timeout_time)

    def set_prop(
        self,
        sys_info_sys_name,
        sys_info_sys_location,
    ):

        set_prop(driver=self.driver,
                 timeout_time=self.timeout_time,
                 logger=self.logger,
                 sys_info_sys_name=sys_info_sys_name,
                 sys_info_sys_location=sys_info_sys_location,
                 tn=self.telnet_instance)

    def check(self, sys_info_sys_name, sys_info_sys_location):
        return check(driver=self.driver,
                     sys_info_sys_name=sys_info_sys_name,
                     sys_info_sys_location=sys_info_sys_location,
                     logger=self.logger,
                     timeout_time=self.timeout_time)

    def quit(self):
        if self.driver:

            self.driver.quit()
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
