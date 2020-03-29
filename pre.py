import os
import re


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        print("---  new folder... ---")
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


def output_txt(path, newline):
    file = open(path, "a+", encoding="utf-8")
    # 转换格式 \转义符号，对"起作用
    file.writelines(newline + "\n")
    file.close()


def fun(path):
    with open('./resource/link.txt', encoding='utf-8') as f:
        for line in f:
            res = re.findall(
                r"href=\"(\/question\/[0-9]+\/answer\/[0-9]+)\">([^<\s]*)<|href=\"\/\/(zhuanlan\.zhihu\.com\/p\/[0-9]+)\"[^>]*>([^<\s]*)<",
                line)  # question
            print(res)
            for eachRes in res:
                for i in range(len(eachRes)):
                    if len(eachRes[i]) > 0:
                        if "question" in eachRes[i]:
                            output_txt(path, 'www.zhihu.com' + str(eachRes[i]))
                        else:
                            output_txt(path, str(eachRes[i]))
                output_txt(path, str(""))

            # for eachRes in res:
            #     if len(eachRes[0]) > 0:
            #         output_txt(path, 'www.zhihu.com' + str(eachRes[0]))
            #     if len(eachRes[1]) > 0:
            #         output_txt(path, str(eachRes[1]))
            #     if len(eachRes[2]) > 0:
            #         output_txt(path, str(eachRes[2]))
            #     if len(eachRes[3]) > 0:
            #         output_txt(path, str(eachRes[3]))
            #

            # res = re.findall(r"href=\"\/\/(zhuanlan.zhihu.com\/p\/[0-9]+)\"[^>]*>([^<]*)<", line)   # zhuanlan
            # print(res)
            # for eachRes in res:
            #     output_txt(path, str(eachRes[0]))
            #     output_txt(path, str(eachRes[1]))


if __name__ == '__main__':
    path = './resource/newLink.txt'
    file = open(path, "w", encoding="utf-8")
    file.close()
    fun(path)
