from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import TimeoutException, NoSuchElementException

import subprocess

import time


def check(driver, sysInfoSysName, sysInfoSysLocation, service, logger):
    try:
        # Menu/SwitchInfo

        switchInfoToggle = driver.find_element(
            By.XPATH,
            '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[2]/tbody/tr/td[3]/a'
        )

        switchInfoToggle.click()

        # switch to iframe

        driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

        # get sysInfoSysName

        _sysInfoSysName = driver.find_element(By.ID, 'sysInfoSysName').text

        # get sysInfoSysLocation

        _sysInfoSysLocation = driver.find_element(By.ID,
                                                  'sysInfoSysLocation').text

        if _sysInfoSysName == sysInfoSysName and _sysInfoSysLocation == sysInfoSysLocation:

            logger.info(
                'expect: %s, got System Name: %s; expect: %s, got System Location: %s'
                % (sysInfoSysName, _sysInfoSysName, sysInfoSysLocation,
                   _sysInfoSysLocation))

        else:

            logger.error(
                'expect: %s, got System Name: %s; expect: %s, got System Location: %s'
                % (sysInfoSysName, _sysInfoSysName, sysInfoSysLocation,
                   _sysInfoSysLocation))

    except Exception as e:

        print('check error')

        raise Exception('check error')

    finally:

        # release resources

        driver.close()
