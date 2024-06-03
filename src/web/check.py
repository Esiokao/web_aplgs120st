from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import TimeoutException, NoSuchElementException

import subprocess
import time


def check(sysInfoSysName, sysInfoSysLocation, service):
    try:
        target_url = 'http://10.3.4.5'

        timeoutTime = 2

        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(10)

        driver.get(target_url)

        try:
            driver.refresh()

            # username input

            username = driver.find_element(By.ID, 'Login')

            username.send_keys("adpro")

            # login button

            loginButton = driver.find_element(By.ID, 'login_ok')

            loginButton.click()

        except NoSuchElementException as e:

            print('No login page displayed')

            return (False, 'no login page')
        try:

            WebDriverWait(driver, 3).until(
                EC.alert_is_present(), 'Timed out waiting for PA creation ' +
                'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()

            print("alert accepted")

        except TimeoutException:

            print("no alert")

            return (False, 'Login failed')
        # root SwitchInfo

        switchInfoToggle = driver.find_element(
            By.XPATH,
            '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[2]/tbody/tr/td[3]/a'
        )

        switchInfoToggle.click()

        # iframe

        driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

        # get sysInfoSysName

        _sysInfoSysName = driver.find_element(By.ID, 'sysInfoSysName').text

        # get sysInfoSysName

        _sysInfoSysLocation = driver.find_element(By.ID,
                                                  'sysInfoSysLocation').text

        if _sysInfoSysName == sysInfoSysName and _sysInfoSysLocation == sysInfoSysLocation:

            return (
                True,
                'expect: %s, got System Name: %s; expect: %s, got System Location: %s'
                % (sysInfoSysName, _sysInfoSysName, sysInfoSysLocation,
                   _sysInfoSysLocation))

        else:

            return (
                False,
                'expect: %s, got System Name: %s; expect: %s, got System Location: %s'
                % (sysInfoSysName, _sysInfoSysName, sysInfoSysLocation,
                   _sysInfoSysLocation))
    except:

        return (False, 'exception occurred')

    finally:

        # release resources

        driver.close()
