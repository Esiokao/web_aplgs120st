from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

import os

import sys

import time

# 獲取當前文件的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))

# 獲取 project 文件夾的絕對路徑
project_dir = os.path.abspath(os.path.join(current_dir, '..'))

# 將 project 文件夾添加到 sys.path 中
sys.path.insert(0, project_dir)

from telnet import telnet


def setProp(driver, timeoutTime, logger, sysInfoSysName, sysInfoSysLocation):

    def toggleMenu():
        try:

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

            time.sleep(timeoutTime)

        except Exception as e:

            print('no menu element detected')

            raise Exception('BAD - No menu element detected')

    def _setProp():

        driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

        try:
            # sysInfoSysName

            sysInfoSysNameInput = driver.find_element(
                By.XPATH,
                '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/input')

            sysInfoSysNameInput.clear()

            sysInfoSysNameInput.send_keys(sysInfoSysName)

            time.sleep(timeoutTime)

            # sysInfoSysLocation

            sysInfoSysLocationInput = driver.find_element(
                By.XPATH,
                '/html/body/form/div/div[2]/table/tbody/tr[4]/td[2]/input')

            sysInfoSysLocationInput.clear()

            sysInfoSysLocationInput.send_keys(sysInfoSysLocation)

            # apply button

            applyBtn = driver.find_element(
                By.XPATH, '/html/body/form/div/div[2]/div[2]/input')

            applyBtn.click()

            logger.info('OK - Set System Name: %s ,  System Location: %s' %
                        (sysInfoSysName, sysInfoSysLocation))

        except Exception as e:

            print('BAD - Setting SystemName failed')

            raise Exception('BAD - Setting SystemName failed')

    def saveConfig():

        # go back to parent content layer

        driver.switch_to.default_content()

        try:
            # save page

            savePageLink = driver.find_element(
                By.XPATH, '/html/body/div/div[2]/div[1]/a')

            savePageLink.click()

            # access to frame layer

            driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

            # save Settings

            saveSettingToFlashBtn = driver.find_element(
                By.XPATH, '/html/body/form/div/div[2]/div/div[2]/input')

            saveSettingToFlashBtn.click()

            # create telnet connection to PSU ahead

            telnetTarget = '192.168.0.60'

            # tn = telnet.createTelnet(telnetTarget)

            # login PSU Management interface

            # telnet.login(tn)

            WebDriverWait(driver, 5).until(
                EC.alert_is_present(), 'Timed out waiting for PA creation ' +
                'confirmation popup to appear.')

            # skip the success message

            # alert = driver.switch_to.alert

            # alert.accept()

            # print("success message accepted")

            # call hook here

            logger.info('OK - save successful alert box detected')

            # wait for 500ms
            time.sleep(timeoutTime)

            start = time.time()

            print('fire hook function')

            # telnet.cutPower(tn)

            end = time.time()

            logger.info('OK - cut off power, time usage: %d ms' % (round(
                (end - start) * 1000)))

            print('time usage: %d ms' % (round((end - start) * 1000)))

        except Exception as e:

            # exception

            print('BAD - Save Config error')

            raise Exception('BAD - Save Config error')

        finally:

            driver.quit()

    try:
        toggleMenu()

        _setProp()

        saveConfig()

    except Exception as e:

        logger.error(e)

        raise Exception('%s error' % __name__)
