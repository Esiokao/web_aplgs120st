from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

import subprocess
import time


def check(sysInfoSysName, sysInfoSysLocation):
    target_url = 'http://10.3.4.5'

    timeoutTime = 2

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.get(target_url)

    # username input

    username = driver.find_element(By.ID, 'Login')

    username.send_keys("adpro")

    # login button

    loginButton = driver.find_element(By.ID, 'login_ok')

    loginButton.click()

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

    time.sleep(timeoutTime)

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

    _sysInfoSysLocation = driver.find_element(By.ID, 'sysInfoSysLocation').text

    driver.quit()

    if _sysInfoSysName == sysInfoSysName and _sysInfoSysLocation == sysInfoSysLocation:
        return True
    else:
        return False
