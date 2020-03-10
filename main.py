# coding=utf-8
import os
import time

from ahk import AHK
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def init():
    # 启用带插件的浏览器
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"C:/Users/ngp/AppData/Local/Google/Chrome/User Data/")
    driver = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe", chrome_options=option)  # 打开chrome浏览器
    driver.maximize_window()
    return driver

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        print ("---  new folder... ---")
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print ("---  OK  ---")
    else:
        print ("---  There is this folder!  ---")

def outputTxt(path,newline):
    file=open(path,"a+", encoding="utf-8")
    #转换格式 \转义符号，对"起作用
    file.writelines(newline+"\n")
    file.close()

def getAllUrl():
    allUrl = []
    with open('./resource/newLink.txt',encoding='utf-8') as f:
        for line in f:
            if("zhuanlan" in line) | ("answer" in line):
                allUrl.append(line.replace('\n', ''))
    print(allUrl)
    return allUrl


def process(driver, url, path):
    driver.get('https://' + url)

    if "question" in url:  # 点击 重排（适用于回答）
        WebDriverWait(driver, 5, 0.5).until(lambda driver: driver.find_element_by_xpath('//a[text()="重排"]'))
        driver.find_element_by_xpath('//a[text()="重排"]').click()
    elif "zhuanlan" in url:  # 点击 重新排版 （适用于专栏）
        WebDriverWait(driver, 5, 0.5).until(lambda driver: driver.find_element_by_xpath('//button[text()="重新排版"]'))
        driver.find_element_by_xpath('//button[text()="重新排版"]').click()
    else:
        return

    driver.find_element_by_tag_name('body').send_keys('`')  # 点击 ` 启动印象笔记剪藏

    # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
    driver.implicitly_wait(10)  # 隐性等待页面 （如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。）
    try:  # 尝试剪藏是否正常
        WebDriverWait(driver, 5, 0.5).until(lambda driver:driver.find_element_by_id('evernoteClipperTools'))  # 显性等待元素 （程序每隔xx秒看以下条件是否满足，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException）
        ahk = AHK()
        ahk.mouse_move(2250, 1050, 30)
        ahk.click()
        ahk.mouse_move(500, 100, 30)
    except Exception:  # 如果剪藏失败
        print('剪藏无法开始：' + url)
        outputTxt(path, '剪藏无法开始：' + url)
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
        except:
            break


    if(countDown==0):
        print('剪藏60s没有结束：' + url)
        outputTxt(path, '剪藏60s没有结束：' + url)
        return

    print('剪藏成功')
    return 2


if __name__ == "__main__":
    path = './resource/error.txt'
    driver = init()
    allUrl = getAllUrl()
    for url in allUrl:
        process(driver, url, path)
    driver.close()
