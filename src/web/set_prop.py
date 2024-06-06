from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


def set_prop(driver, timeout_time, logger, sys_info_sys_name,
             sys_info_sys_location, tn):

    def toggle_menu():

        try:
            print(f'handling toggle_menu...')
            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[3]/tbody/tr/td[3]/a'
                )))
            menu_sys_ele = driver.find_element(
                By.XPATH,
                '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/table[3]/tbody/tr/td[3]/a'
            )
            menu_sys_ele.click()

            time.sleep(timeout_time)

            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/div[1]/table[1]/tbody/tr/td[3]/a'
                )))

            menu_sys_manager_ele = driver.find_element(
                By.XPATH,
                '/html/body/div/div[3]/div/table/tbody/tr/td[1]/div/div/div/div/div[1]/table[1]/tbody/tr/td[3]/a'
            )

            menu_sys_manager_ele.click()

        except NoSuchElementException as e:
            raise Exception(__name__, 'Menu System element not detected')

    def _set_prop():

        try:
            print(f'handling _set_prop...')
            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located((By.ID, "myframe")))

            driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/input'
                     )))

            sys_info_sys_name_input = driver.find_element(
                By.XPATH,
                '/html/body/form/div/div[2]/table/tbody/tr[3]/td[2]/input')

            sys_info_sys_name_input.clear()

            sys_info_sys_name_input.send_keys(sys_info_sys_name)

            time.sleep(timeout_time)

            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/form/div/div[2]/table/tbody/tr[4]/td[2]/input'
                     )))

            sys_info_sys_location_input = driver.find_element(
                By.XPATH,
                '/html/body/form/div/div[2]/table/tbody/tr[4]/td[2]/input')

            sys_info_sys_location_input.clear()

            sys_info_sys_location_input.send_keys(sys_info_sys_location)

            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/form/div/div[2]/div[2]/input')))

            apply_btn = driver.find_element(
                By.XPATH, '/html/body/form/div/div[2]/div[2]/input')

            apply_btn.click()

            logger.info('OK - Set System Name: %s ,  System Location: %s' %
                        (sys_info_sys_name, sys_info_sys_location))

        except NoSuchElementException as e:
            raise Exception(__name__, 'Set property failed') from e
        except Exception as e:
            raise Exception(__name__, e) from e

    def save_config():
        try:
            print(f'handling save_config...')

            driver.switch_to.parent_frame()

            tn.connect()

            tn.login()

            save_page_link = driver.find_element(
                By.XPATH, '/html/body/div/div[2]/div[1]/a')

            save_page_link.click()

            driver.switch_to.frame(driver.find_element(By.ID, "myframe"))

            save_setting_to_flash_btn = driver.find_element(
                By.XPATH, '/html/body/form/div/div[2]/div/div[2]/input')

            save_setting_to_flash_btn.click()

            WebDriverWait(driver, 5).until(EC.alert_is_present())

            alert = driver.switch_to.alert

            alert.accept()

            logger.info('OK - save successful alert box detected')

            start = time.time()

            # TODO: subscriber pattern or hook

            tn.cut_power()

            end = time.time()

            logger.info('OK - cut off power, time usage: %d ms' % (round(
                (end - start) * 1000)))

            tn.close()

        except NoSuchElementException as e:
            print(e)
            raise Exception(
                __name__,
                'Exception occurred : NoSuchElementException ') from e
        except TimeoutException as e:
            print(e)
            raise Exception(__name__, 'Exception occurred : Time out ') from e
        except Exception as e:
            print(e)
            raise Exception(__name__, e) from e

    try:

        toggle_menu()
        _set_prop()
        save_config()

    except Exception as e:
        raise
