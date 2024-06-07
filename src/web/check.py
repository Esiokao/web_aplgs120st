from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def check(driver, sys_info_sys_name, sys_info_sys_location, logger,
          timeout_time):
    try:
        time.sleep(timeout_time)
        print('checking result...')

        try:
            # Menu/SwitchInfo
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[2]/tbody/tr/td[3]/a'
                )), 'Menu/SwitchInfo')
        except TimeoutException as e:
            raise Exception(__name__, e)

        switchInfoToggleEle = driver.find_element(
            By.XPATH,
            '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[2]/tbody/tr/td[3]/a'
        )

        switchInfoToggleEle.click()

        # switch to iframe
        driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

        # get sys_info_sys_name
        _sys_info_sys_name = driver.find_element(By.ID, 'sysInfoSysName').text

        # get sysInfoSysLocation
        _sys_info_sys_location = driver.find_element(By.ID,
                                                     'sysInfoSysLocation').text

        if _sys_info_sys_name == sys_info_sys_name and _sys_info_sys_location == sys_info_sys_location:
            logger.info(
                'OK - expect: %s, got System Name: %s; expect: %s, got System Location: %s'
                % (sys_info_sys_name, _sys_info_sys_name,
                   sys_info_sys_location, _sys_info_sys_location))

            return True
        elif _sys_info_sys_name[-2:] == sys_info_sys_name[
                -2:] and _sys_info_sys_location[-2:] == sys_info_sys_location[
                    -2:]:
            # check if last words is same last time configured, may due to configs didn't get saved.
            logger.warning(
                f'WARN - got previous time configuration: System Name: {_sys_info_sys_name}, System location: {_sys_info_sys_location}'
            )
            return True
        else:
            logger.error(
                'error - expect: %s, got System Name: %s; expect: %s, got System Location: %s'
                % (sys_info_sys_name, _sys_info_sys_name,
                   sys_info_sys_location, _sys_info_sys_location))

            return False
    except Exception as e:
        raise Exception(__name__, e)
