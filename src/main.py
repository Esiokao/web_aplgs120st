from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

import subprocess
import time

from utils.change_ipAddr import change_ipAddr

from telnet.disconnect import disconnect, login

from web.check import check

# switch預設IP: 10.3.4.5

target_url = 'http://10.3.4.5'

timeoutTime = 2

sysName = 'someRandomName1'

sysLocation = 'someRandomLocation2'

# sec
reboot_stall_timeout = 110
# change_ipAddr("eth1", "10.0.0.1", "255.0.0.0", "10.0.0.254")

time.sleep(timeoutTime)

# def get_installed_chromedriver_version():

#     driver_path = ChromeDriverManager().install()

#     version = subprocess.check_output([driver_path,

#                                        '--version']).decode('utf-8').strip()

#     return version

# version = get_installed_chromedriver_version()

# print(f"Installed ChromeDriver version: {version}")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get(target_url)

print(driver.title)

# username input

username = driver.find_element(By.ID, 'Login')

username.send_keys("adpro")

# login button

loginButton = driver.find_element(By.ID, 'login_ok')

loginButton.click()

time.sleep(timeoutTime)

try:

    WebDriverWait(driver, 3).until(
        EC.alert_is_present(),
        'Timed out waiting for PA creation ' + 'confirmation popup to appear.')

    alert = driver.switch_to.alert
    alert.accept()

    print("alert accepted")

except TimeoutException:

    print("no alert")

time.sleep(timeoutTime)

# root System

menuSysEle = driver.find_element(
    By.XPATH,
    '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[3]/tbody/tr/td[3]/a'
)

menuSysEle.click()

time.sleep(timeoutTime)

# root System System Management

menuSysManagerEle = driver.find_element(
    By.XPATH,
    '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/div[1]/table[1]/tbody/tr/td[3]/a'
)

menuSysManagerEle.click()

time.sleep(timeoutTime)

driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

# sysInfoSysName

sysInfoSysNameInput = driver.find_element(
    By.XPATH, '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/input')

sysInfoSysNameInput.clear()

sysInfoSysNameInput.send_keys(sysName)

time.sleep(timeoutTime)

# sysInfoSysLocation

sysInfoSysLocationInput = driver.find_element(
    By.XPATH, '/html/body/form/div/div[2]/table/tbody/tr[4]/td[2]/input')

sysInfoSysLocationInput.clear()

sysInfoSysLocationInput.send_keys(sysLocation)

time.sleep(timeoutTime)

# apply button

applyBtn = driver.find_element(By.XPATH,
                               '/html/body/form/div/div[2]/div[2]/input')

applyBtn.click()

time.sleep(timeoutTime)

# go back to parent content layer

driver.switch_to.default_content()

# save page

savePageLink = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/a')

savePageLink.click()

# access to frame layer

driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

# save Settings

saveSettingToFlashBtn = driver.find_element(
    By.XPATH, '/html/body/form/div/div[2]/div/div[2]/input')

saveSettingToFlashBtn.click()

try:
    login()
    WebDriverWait(driver, 3).until(
        EC.alert_is_present(),
        'Timed out waiting for PA creation ' + 'confirmation popup to appear.')

    # skip the success message

    # alert = driver.switch_to.alert

    # alert.accept()

    # print("success message accepted")

    # call hook here

    start = time.time()

    print('fire hook function')
    disconnect()

    end = time.time()

    print('time usage: %.3f ms' % (end - start))

except TimeoutException:

    # expection

    print("no alert")

driver.quit()

time.sleep(reboot_stall_timeout)

result = check(sysInfoSysName=sysName, sysInfoSysLocation=sysLocation)

print('match result', result)
