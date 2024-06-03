from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

import time


def login(driver, targetUrl, pageTitle, username, logger, timeoutTime):

    loginCounter = 0

    status = True

    # refresh

    def connect(counter):

        counter += 1

        driver.get(targetUrl)

        title = driver.title

        if pageTitle in driver.title:

            logger.info('OK - Http request ok')

        else:

            if counter <= 3:

                driver.refresh()

                connect()

            else:

                logger.error('Bad - Bad request')

                return (False, 'Bad - Bad request')

    def fillLoginField():

        try:

            # fill username input field

            username = driver.find_element(By.ID, 'Login')

            username.send_keys("adpro")

            # click login button

            loginButton = driver.find_element(By.ID, 'login_ok')

            loginButton.click()

        except NoSuchElementException as e:

            print('no login filed element detected')

            raise Exception('no login filed element detected')

        finally:

            time.sleep(timeoutTime)

    def passwordAlertCheck():

        try:

            WebDriverWait(driver, 3).until(
                EC.alert_is_present(), 'Timed out waiting for PA creation ' +
                'confirmation popup to appear.')

            alert = driver.switch_to.alert

            alert.accept()

            print("password alert accepted")

        except TimeoutException as e:

            print("no password alert")

            raise Exception('no password alert box detected')

    try:
        connect(loginCounter)

        fillLoginField()

        passwordAlertCheck()

    except Exception as e:

        logger.error(e)

        raise Exception('login phase error')
