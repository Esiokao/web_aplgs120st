from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from utils.change_ipAddr import change_ipAddr

from web import login, setProp, check

from utils.randChar import randChar

import web

import subprocess

import time

import logging

from datetime import datetime

# switch預設IP: 10.3.4.5

target_url = 'http://10.3.4.5'

timeoutTime = 2

reboot_stall_timeout = 100  # sec

service = Service(ChromeDriverManager().install())

# change_ipAddr("eth1", "10.0.0.1", "255.0.0.0", "10.0.0.254")

# time.sleep(timeoutTime)

# def get_installed_chromedriver_version():

#     driver_path = ChromeDriverManager().install()

#     version = subprocess.check_output([driver_path,

#                                        '--version']).decode('utf-8').strip()

#     return version

# version = get_installed_chromedriver_version()

# print(f"Installed ChromeDriver version: {version}")

for i in range(5):

    # 取得目前時間
    current_time = datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # attemptTime = 'attempt'

    fileName = formatted_time + '.log'

    logging.basicConfig(level=logging.INFO,
                        filename=fileName,
                        filemode="w+",
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logger = logging.getLogger(str(i))

    for j in range(100):

        print(str(j + 1) + '\n')

        logger.info('attempt %d -' % (j + 1))

        sysName = randChar(10) + "%02d" % (j + 1)

        sysLocation = randChar(10) + "%02d" % (j + 1)

        # extractable

        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(10)
        try:

            login.login(driver=driver,
                        targetUrl=target_url,
                        pageTitle='Login',
                        username='adpro',
                        logger=logger,
                        timeoutTime=.5)

            setProp.setProp(
                driver=driver,
                logger=logger,
                timeoutTime=.5,
                sysInfoSysName=sysName,
                sysInfoSysLocation=sysLocation,
            )

            time.sleep(reboot_stall_timeout)

            login.login(driver=driver,
                        targetUrl=target_url,
                        pageTitle='Login',
                        username='adpro',
                        logger=logger,
                        timeoutTime=.5)

            check.check(driver=driver,
                        logger=logger,
                        sysInfoSysName=sysName,
                        sysInfoSysLocation=sysLocation,
                        service=service)

        except Exception as e:

            pass

        finally:

            if driver != None:

                driver.close()
