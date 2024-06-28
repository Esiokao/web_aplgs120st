import logging

import time

from datetime import datetime

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service

from web.Web import Web

from telnet.TelnetConnection import TelnetConnection

from utils.randChar import randChar

from retrying import retry
#

DEFAULT_URL = 'http://10.3.4.5'

TARGET_URL = 'http://10.3.4.5'

TELNET_TARGET = '192.168.0.60'

TELNET_PORT = 23

TIMEOUT_TIME = 3  # second

IMPLICITLY_WAIT_TIME = 5

REBOOT_STALL_TIMEOUT = 110  # second

NUM_ATTEMPTS = 1500

MAX_CONTINUOUS_ERRORS = 3

# 初始化ChromeDriver

service = Service(ChromeDriverManager().install())


def setup_logging():

    current_time = datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    fileName = formatted_time + '.log'

    logging.basicConfig(level=logging.INFO,
                        filename=fileName,
                        filemode="w+",
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    return logging.getLogger('logger')


def main():

    logger = setup_logging()

    tn = TelnetConnection(TELNET_TARGET, TELNET_PORT)

    continuous_errors = 0

    for attempt in range(NUM_ATTEMPTS):

        print(f"Attempt {attempt + 1}\n")

        logger.info(f'Attempt {attempt + 1} -')

        sysName = randChar(10) + f"{attempt + 1:02d}"

        sysLocation = randChar(10) + f"{attempt + 1:02d}"

        try:

            # create instance

            web_instance = Web(logger=logger,
                               service=service,
                               implicitly_wait_time=IMPLICITLY_WAIT_TIME,
                               target_url=TARGET_URL,
                               timeout_time=TIMEOUT_TIME,
                               telnet_instance=tn)

            # login DUT

            web_instance.login(username='adpro', page_title='Login')

            # setup property of DUT

            set_prop_result = web_instance.set_prop(
                sys_info_sys_name=sysName, sys_info_sys_location=sysLocation)

            if set_prop_result == False:

                break

            web_instance.quit()

            time.sleep(REBOOT_STALL_TIMEOUT)

            @retry(stop_max_attempt_number=3,
                   wait_fixed=1000 * 5,
                   before_attempts=lambda retry_state: print(
                       f"Retrying: login_Then_check..\n"))
            def login_Then_check():

                # reinitialize webdriver instance

                web_instance.init_driver(
                    service=service, implicitly_wait_time=IMPLICITLY_WAIT_TIME)

                # login again

                web_instance.login(username='adpro', page_title='Login')

                # return True/ False

                result = web_instance.check(sys_info_sys_name=sysName,
                                            sys_info_sys_location=sysLocation)

                web_instance.quit()

                return result

            check_result = login_Then_check()

            if check_result == False:

                break

            # reset error coUnters
            continuous_errors = 0

        except Exception as e:

            continuous_errors += 1

            print('exception occurred')

            logger.error(f'Error : {e}')

            print(e)

            if continuous_errors >= MAX_CONTINUOUS_ERRORS:
                logger.error(
                    f'error occurred over {MAX_CONTINUOUS_ERRORS} times, main process stopped.'
                )
                break

        finally:

            web_instance.quit()


if __name__ == '__main__':

    main()
