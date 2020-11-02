import random
import time

import selenium.webdriver.support.ui as ui
import urllib3
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 一直等待某元素可见，默认超时10秒
def wait_to_visible(driver, Xpath: str, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, Xpath)))
        return True
    except TimeoutException:
        return False


def Xpath_wait_click_or_input(driver, xpath: str, sendKeys=None, timeout=None):
    try:
        if timeout is not None:
            wait_to_visible(driver, xpath, timeout=timeout)
        else:
            wait_to_visible(driver, xpath)
        if sendKeys is None:
            driver.find_element_by_xpath(xpath).click()
        else:
            driver.find_element_by_xpath(xpath).send_keys(sendKeys)
    except Exception:
        raise

def xpathGetText(driver, xpath)->str:
    return driver.find_element_by_xpath(xpath).text

def randomSleep(maxRandomDIY=None):
    maxRandom = 2
    if maxRandomDIY is not None:
        maxRandom = maxRandomDIY
    time.sleep(1)
    # 生成随机数，浮点类型
    a = random.uniform(0, maxRandom)
    # 控制随机数的精度round(数值，精度)
    num = round(a, 1)
    time.sleep(num)
