# coding=utf-8
import logging
import logging.config
import os
import time

import yaml
from ahk import AHK
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


def init():
    # 启用带插件的浏览器
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"C:/Users/ngp/AppData/Local/Google/Chrome/User Data/")
    # driver = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe")     # 打开chrome浏览器
    driver = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe", chrome_options=option)  # 打开有插件的chrome浏览器
    driver.maximize_window()
    return driver


def getAllUrl():
    allUrl = []
    with open('./resource/newLink.txt', encoding='utf-8') as f:
        for line in f:
            if("zhuanlan" in line) | ("answer" in line):
                allUrl.append(line.replace('\n', ''))
    logging.info(allUrl)
    return allUrl


def process(driver, url):
    driver.get('https://' + url)

    if "question" in url:  # 点击 重排（适用于回答）
        xpath_content = '//a[text()="重排"]'
    elif "zhuanlan" in url:  # 点击 重新排版 （适用于专栏）
        xpath_content = '//button[text()="重新排版"]'

    try:
        time.sleep(1)   #强制等待1s
        WebDriverWait(driver, 5, 0.5).until(lambda driver: driver.find_element_by_xpath(xpath_content))
    except TimeoutException as e:
        logging.error("异常 没有找到元素 : ", str(e))
        return
    except Exception as e:
        logging.error("异常 : ", str(e))
        return

    logging.info(driver.find_element_by_xpath(xpath_content).click())     # 点击 重排/重新排版
    driver.find_element_by_tag_name('body').send_keys('`')  # 点击 ` 启动印象笔记剪藏

    # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
    driver.implicitly_wait(10)  # 隐性等待页面 （如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。）
    try:  # 尝试剪藏是否正常
        WebDriverWait(driver, 5, 0.5).until(lambda driver:driver.find_element_by_id('evernoteClipperTools'))  # 显性等待元素 （程序每隔xx秒看以下条件是否满足，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException）
        driver.switch_to_frame("evernoteClipperTools")  #切换到 嵌入iframe代码
        WebDriverWait(driver, 5, 0.5).until(lambda driver:driver.find_element_by_xpath('//button[text()="保存剪藏"]'))  # 显性等待元素 （程序每隔xx秒看以下条件是否满足，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException）
        ahk = AHK()
        ahk.mouse_move(2250, 1050, 30)
        ahk.click()
        ahk.mouse_move(500, 100, 30)
        driver.switch_to.default_content()  #切换到 主页代码
    except NoSuchElementException as e:  # 如果剪藏失败
        logging.error('剪藏无法开始：' + url + str(e))
        return
    except Exception as e:
        logging.error("异常 : ", str(e))
        return

    #因为WebDriverWait失效，所以利用ahk手动点击空白处使弹窗消失，以触发剪藏下一个网址的动作
    countDown = 60
    while countDown :
        try:
            driver.find_element_by_id('evernoteClipperTools')
            ahk.mouse_move(10, 20 * countDown, 30)
            ahk.click()
            time.sleep(1)
            countDown = countDown - 1
        except Exception as e:
            logging.error("异常 : ", str(e))
            break   #如果没有则跳出while


    if(countDown==0):
        logging.error('剪藏60s没有结束：' + url)
        return

    logging.info('剪藏成功' + url)
    return 2



if __name__ == "__main__":
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f)
        logging.config.dictConfig(config)
    driver = init()
    allUrl = getAllUrl()
    for url in allUrl:
        process(driver, url)
    driver.close()
