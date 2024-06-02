from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from telnet.disconnect import login, disconnect, createTelnet

from utils.change_ipAddr import change_ipAddr

from utils.rand_char import random_char

from web.check import check

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


def createService(sysName, sysLocation):

    driver = webdriver.Chrome(service=service)

    driver.implicitly_wait(10)

    driver.get(target_url)

    driver.refresh()

    title = driver.title

    if title == 'Login':

        logger.info('OK - Http request ok')

    else:

        logger.error('Bad - Bad request')

        return

    try:

        # fill username input field

        username = driver.find_element(By.ID, 'Login')

        username.send_keys("adpro")

        # click login button

        loginButton = driver.find_element(By.ID, 'login_ok')

        loginButton.click()

    except NoSuchElementException as e:

        print(e)

        return

    time.sleep(timeoutTime)

    try:

        WebDriverWait(driver, 3).until(
            EC.alert_is_present(), 'Timed out waiting for PA creation ' +
            'confirmation popup to appear.')

        alert = driver.switch_to.alert

        alert.accept()

        print("alert accepted")

    except TimeoutException:

        print("no alert")

        return

    time.sleep(timeoutTime)

    # menu/System

    menuSysEle = driver.find_element(
        By.XPATH,
        '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[3]/tbody/tr/td[3]/a'
    )

    menuSysEle.click()

    time.sleep(timeoutTime)

    # menu/System/System Management

    menuSysManagerEle = driver.find_element(
        By.XPATH,
        '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/div[1]/table[1]/tbody/tr/td[3]/a'
    )

    menuSysManagerEle.click()

    # time.sleep(timeoutTime)

    driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

    try:
        # sysInfoSysName

        sysInfoSysNameInput = driver.find_element(
            By.XPATH,
            '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/input')

        sysInfoSysNameInput.clear()

        sysInfoSysNameInput.send_keys(sysName)

        time.sleep(timeoutTime)

        # sysInfoSysLocation

        sysInfoSysLocationInput = driver.find_element(
            By.XPATH,
            '/html/body/form/div/div[2]/table/tbody/tr[4]/td[2]/input')

        sysInfoSysLocationInput.clear()

        sysInfoSysLocationInput.send_keys(sysLocation)

        logger.info('OK - Set System Name: %s ,  System Location: %s' %
                    (sysName, sysLocation))
    except:

        logger.error('BAD - Setting SystemName failed')

    # time.sleep(timeoutTime)

    # apply button

    applyBtn = driver.find_element(By.XPATH,
                                   '/html/body/form/div/div[2]/div[2]/input')

    applyBtn.click()

    # time.sleep(timeoutTime)

    # go back to parent content layer

    driver.switch_to.default_content()

    try:
        # save page

        savePageLink = driver.find_element(By.XPATH,
                                           '/html/body/div/div[2]/div[1]/a')

        savePageLink.click()

        # access to frame layer

        driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

        # save Settings

        saveSettingToFlashBtn = driver.find_element(
            By.XPATH, '/html/body/form/div/div[2]/div/div[2]/input')

        saveSettingToFlashBtn.click()

        # create telnet connection to PSU ahead

        tn = createTelnet()

        # login PSU Management interface

        login(tn)

        WebDriverWait(driver, 5).until(
            EC.alert_is_present(), 'Timed out waiting for PA creation ' +
            'confirmation popup to appear.')

        # skip the success message

        # alert = driver.switch_to.alert

        # alert.accept()

        # print("success message accepted")

        # call hook here

        logger.info('OK - save successful alert box detected')

        start = time.time()

        print('fire hook function')

        disconnect(tn)

        end = time.time()

        logger.info('OK - cut off power, time usage: %d ms' % (round(
            (end - start) * 1000)))

        print('time usage: %d ms' % (round((end - start) * 1000)))

    except Exception as e:

        # expection

        logger.exception(e)

        return

    driver.quit()


for i in range(5):

    # 取得目前時間
    current_time = datetime.now()

    # 以指定格式生成時間字符串
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # attemptTime = 'attempt'

    fileName = formatted_time + '.log'

    formatter = logging.Formatter()

    logging.basicConfig(level=logging.INFO,
                        filename=fileName,
                        filemode="w+",
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logger = logging.getLogger()

    for j in range(100):

        logger.info('attempt %d -' % j)

        sysName = random_char(10) + "%02d" % (j + 1)

        sysLocation = random_char(10) + "%02d" % (j + 1)

        createService(sysName=sysName, sysLocation=sysLocation)

        time.sleep(reboot_stall_timeout)

        status, result = check(sysInfoSysName=sysName,
                               sysInfoSysLocation=sysLocation,
                               service=service)

        if status != True:

            logger.error('BAD - reboot check : %s' % result)
        else:

            logger.info('OK - reboot check : %s' % result)
