from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException
import time


def login(driver, target_url, page_title, username, logger, timeout_time):
    login_counter = 0
    max_retries = 3
    refresh_interval = 5

    def connect():
        nonlocal login_counter
        print(f'handling connect...')

        while login_counter <= max_retries:
            # break condition
            login_counter += 1

            try:
                driver.get(target_url)
                # driver.get(target_url)
                if page_title in driver.title:

                    logger.info('OK - Http request ok')

                    return True
                else:

                    raise Exception(__name__,
                                    'Page title does not match, Wrong Page')

            except Exception as e:

                print(f'Retry {login_counter}')

                time.sleep(refresh_interval)

                driver.refresh()

        raise Exception(__name__,
                        f'Bad http request after {login_counter} attempts')

    def fill_login_field():
        try:
            print(f'handling fill_login_field...')
            time.sleep(timeout_time)
            WebDriverWait(driver, timeout_time).until(
                EC.presence_of_element_located((By.ID, 'Login')))

            username_field = driver.find_element(By.ID, 'Login')
            username_field.send_keys(username)
            login_button = driver.find_element(By.ID, 'login_ok')
            login_button.click()

        except NoSuchElementException as e:
            raise Exception(
                __name__, 'Login phase error, Login form not detected') from e

    def handle_password_alert():
        try:
            print(f'handling handle_password_alert...')
            time.sleep(timeout_time)
            WebDriverWait(driver, timeout_time).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print("OK - Password alert accepted")

        except TimeoutException:
            pass

        except NoAlertPresentException:
            pass  # No alert present, nothing to handle

    try:
        connect()
        fill_login_field()
        # Uncomment if you need to handle password alert
        handle_password_alert()
    except Exception as e:
        raise
