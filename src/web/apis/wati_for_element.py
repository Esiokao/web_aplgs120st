from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def wait_for_element_by_xpath(driver, xpath, timeout=10):
    """
    等待指定的元素通過XPath加載完成。

    參數:
    driver (webdriver): WebDriver實例
    xpath (str): 元素的XPath
    timeout (int): 等待超時時間（秒）

    返回:
    bool: 如果元素加載完成返回True，否則返回False
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False
