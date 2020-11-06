# coding=utf-8
import logging
import logging.config
import shutil
import time
import traceback

from selenium.webdriver.common.keys import Keys
import yaml

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from utils.utils import wait_to_visible, Xpath_wait_click_or_input, xpathGetText, randomSleep


def init():
    # 调用config.yaml里的 logging配置
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f)
        logging.config.dictConfig(config)
    # 启用带插件的浏览器
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"C:/Users/ngp/AppData/Local/Google/Chrome/User Data/")
    # driver = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe")     # 打开chrome浏览器
    driver = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe", chrome_options=option)  # 打开有插件的chrome浏览器
    # driver.maximize_window()
    return driver


def getAllUrl():
    allUrl = []
    allTitle = []
    with open('./resource/newLink.txt', encoding='utf-8') as f:
        lines = reversed(f.readlines())  # 从最后一行, 开始读,这样剪藏的时间顺序对得上
        for line in lines:
            if ("zhuanlan" in line) | ("answer" in line):
                allUrl.append(line.replace('\n', ''))

    logging.info('allUrl: ' + str(allUrl[0:5]) + "......")
    return allUrl


def zhihu_process(driver, url, recursion):
    # 打开网页
    driver.get('https://' + url)

    if "question" in url:  # 点击 重排（适用于回答）
        xpath_content = '//a[text()="重排"]'
    elif "zhuanlan" in url:  # 点击 重新排版 （适用于专栏）
        xpath_content = '//button[text()="重新排版"]'
    driver.implicitly_wait(10)  # 隐性等待页面 #值得注意的是 隐性等待和显性等待的最长时间取两者之中的大者
    try:
        WebDriverWait(driver, 20, 0.5).until(lambda driver: driver.find_element_by_xpath(xpath_content))  # 寻找重排
    except TimeoutException:
        logging.error("TimeoutException 没有找到元素 : \n%s", traceback.format_exc())
        if recursion > 0:
            logging.info("剪藏失败，倒数第%s次尝试", recursion)
            zhihu_process(driver, url, recursion - 1)
        else:
            return
    except Exception:
        logging.error('Exception : \n%s', traceback.format_exc())
        return
    # .click失效 换用js
    # driver.find_element_by_xpath(xpath_content).click()     # 点击 重排/重新排版
    if "question" in url:  # 点击 重排（适用于回答）
        jsClick = "document.getElementsByClassName('Tabs-link AppHeader-TabsLink')[4].click();"
        driver.execute_script(jsClick)
    elif "zhuanlan" in url:  # 点击 重新排版 （适用于专栏）
        jsClick = "document.getElementsByClassName('Button Button--blue')[0].click();"
        driver.execute_script(jsClick)

    driver.find_element_by_tag_name('body').send_keys('`')  # 热键启动印象笔记剪藏

    # 点击开始剪藏
    driver.implicitly_wait(10)  # 隐性等待页面 #值得注意的是 隐性等待和显性等待的最长时间取两者之中的大者
    try:  # 尝试剪藏是否正常
        wait_to_visible(driver, '//*[@id="evernoteClipperTools"]')
        randomSleep()
        driver.switch_to.frame("evernoteClipperTools")  # 切换到 嵌入iframe代码
        randomSleep()
        # Xpath_wait_click_or_input(driver, '//div[@class="ClipperContainer"]//div[text()="整个页面"]')
        # randomSleep()
        noteName = xpathGetText(driver,'//div[@class="ClipperContainer"]//div[@class="itemTitle"]')
        # print(noteName)
        if not noteName.startswith('z知乎'):
            raise SystemExit("请把 剪藏存储文件夹设为 z知乎 后重试")
        modeName = xpathGetText(driver, '//div[contains(@class,"checkIcon check")]/../..')
        if not modeName.startswith('整个页面'):
            raise SystemExit("请把 剪藏模式设为 整个页面 后重试")
        # 有时点击会无效 =.=
        # if noteName.startswith('z知乎'):
        #     pass
        # else:
        #     # 没有在这个分类就划入这个分类
        #     Xpath_wait_click_or_input(driver, '//div[@class="selectorCaretIcon"]')
        #     Xpath_wait_click_or_input(driver, '//div[@class="children"]//div[contains(@class, "withoutCollapse") and @title="z知乎"]')
        # randomSleep()
        #
        # Xpath_wait_click_or_input(driver, '//button[text()="保存剪藏"]')
        # .click失效 换用ahk
        # ahk.
        # driver.find_element_by_xpath('//button[text()="保存剪藏"]').click()
        # jsClick = "document.getElementsByClassName('saveButton variantB')[0].click();"
        # driver.execute_script(jsClick)
        driver.switch_to.default_content()  # 切换到 主页代码

        # 通过代码 完善了 切换iframe... 那么selenium的热键enter也注释掉, 可以备用.
        body = driver.find_element_by_xpath("//body")
        body.send_keys(Keys.ENTER)

        # ahk = AHK()
        # ahk.find_windows_by_title("Google Chrome")
        # ahk.key_press("enter")
    except NoSuchElementException:  # 如果剪藏失败
        logging.error('NoSuchElementException 剪藏无法开始：', traceback.format_exc() + url)
        if recursion > 0:
            logging.info("剪藏失败，倒数第%s次尝试", recursion)
            zhihu_process(driver, url, recursion - 1)
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

    allUrl = getAllUrl()

    print("正在启动WebDriver...")
    driver = init()
    print("启动完毕... 开始剪藏...")
    print("\t请先 确定知乎 没有 (1条消息)...\n"
          "\t并开启chrome扩展的 zhihu-clipper模式, 尽量关闭 油猴+印象笔记 以外的插件, 以免相互影响\n"
          "\t并确认 印象笔记 调到了 整个页面+剪藏到z知乎文件夹(有代码检测, 不是这个程序会停止运行)\n")
    for url in allUrl:
        zhihu_process(driver, url, 3)  # 找不到排版 最多刷新三次
    driver.quit()

    shutil.copyfile("resource/newlink.txt", "resource/last_time_newlink.txt")
