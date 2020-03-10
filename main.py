# coding=utf-8
import logging
import logging.config
import time
import traceback

import yaml
from ahk import AHK
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


def init():
    #调用config.yaml里的 logging配置
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f)
        logging.config.dictConfig(config)
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
    logging.info('allUrl: ' + str(allUrl[0:5]) + "......")
    return allUrl


def process(driver, url, recursion):
    # 打开网页
    driver.get('https://' + url)
    # 点击 重排/开始重排
    if "question" in url:  # 点击 重排（适用于回答）
        xpath_content = '//a[text()="重排"]'
    elif "zhuanlan" in url:  # 点击 重新排版 （适用于专栏）
        xpath_content = '//button[text()="重新排版"]'
    driver.implicitly_wait(10)  # 隐性等待页面 #值得注意的是 隐性等待和显性等待的最长时间取两者之中的大者
    try:
        WebDriverWait(driver, 5, 0.5).until(lambda driver: driver.find_element_by_xpath(xpath_content)) # 寻找重排
    except TimeoutException:
        logging.error("TimeoutException 没有找到元素 : \n%s", traceback.format_exc())
        if recursion > 0:
            logging.info("剪藏失败，倒数第%s次尝试", recursion)
            process(driver, url, recursion - 1)
        else:
            return
    except Exception:
        logging.error('Exception : \n%s', traceback.format_exc())
        return
    driver.find_element_by_xpath(xpath_content).click()     # 点击 重排/重新排版
    driver.find_element_by_tag_name('body').send_keys('`')  # 热键启动印象笔记剪藏

    # 点击开始剪藏
    driver.implicitly_wait(10)  # 隐性等待页面 #值得注意的是 隐性等待和显性等待的最长时间取两者之中的大者
    try:  # 尝试剪藏是否正常
        WebDriverWait(driver, 5, 0.5).until(lambda driver:driver.find_element_by_id('evernoteClipperTools'))  # 显性等待元素 （程序每隔xx秒看以下条件是否满足，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException）
        driver.switch_to.frame("evernoteClipperTools")  #切换到 嵌入iframe代码
        WebDriverWait(driver, 5, 0.5).until(lambda driver:driver.find_element_by_xpath('//button[text()="保存剪藏"]'))  # 点击 保存剪藏
        time.sleep(1)
        driver.find_element_by_xpath('//button[text()="保存剪藏"]').click()
        driver.switch_to.default_content()  # 切换到 主页代码
    except NoSuchElementException:  # 如果剪藏失败
        logging.error('NoSuchElementException 剪藏无法开始：', traceback.format_exc() + url)
        if recursion > 0:
            logging.info("剪藏失败，倒数第%s次尝试", recursion)
            process(driver, url, recursion - 1)
        else:
            return
    except Exception:
        logging.error('Exception : \n%s', traceback.format_exc())
        return



    # 检测到 剪藏完成则开始剪藏下一个页面
    try:  # 尝试剪藏是否完成
        WebDriverWait(driver, 5, 0.5).until(lambda driver: driver.find_element_by_id('evernoteClipperTools'))
        driver.switch_to.frame("evernoteClipperTools")  # 切换到 嵌入iframe代码
        WebDriverWait(driver, 60, 0.5).until(lambda driver: driver.find_element_by_xpath(
            '//a[text()="Evernote 中的视图"]'))
        # ahk = AHK()
        # ahk.mouse_move(2200, 450, 30)   # 如果剪藏完成动一下鼠标，测试的时候方便肉眼判断
        # ahk.mouse_move(300, 100, 50)    # 如果剪藏完成动一下鼠标，测试的时候方便肉眼判断
        driver.switch_to.default_content()  # 切换到 主页代码
    except NoSuchElementException:  # 如果剪藏失败
        logging.error('NoSuchElementException 剪藏60s无法完成 ：\n%s', traceback.format_exc() + '\n' + url)
        return
    except Exception:
        logging.error('Exception : \n%s', traceback.format_exc())
        return

    logging.info('剪藏成功 : ' + url)
    return 2



if __name__ == "__main__":
    driver = init()
    allUrl = getAllUrl()
    for url in allUrl:
        process(driver, url, 3) #找不到排版 最多刷新三次
    driver.close()
