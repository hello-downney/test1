import requests
import re
import time
import random
import os
os.mkdir(r"C:\Users\admin\Desktop\tupian")#创建一个文件夹存储资源

from concurrent.futures import ThreadPoolExecutor#多线程


obj1 = re.compile(r'<h2><a.*?href="(?P<urls>.*?)">.*?</a></h2>',re.S)
obj2 = re.compile(r'<img decoding="async" src=.*?data-src="(?P<imgs>.*?)" alt=',re.S)

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "referer":"https://www.moetu.club/",
    "cookie":"_gid=GA1.2.923017178.1758639251; Hm_lvt_8f6576f1c707a7b6b7a3b499135768e6=1758639248,1758676954,1758685757,1758699120; HMACCOUNT=FB479BE85C086A64; _gat_gtag_UA_120802358_2=1; Hm_lpvt_8f6576f1c707a7b6b7a3b499135768e6=1758699127; _ga_EBCMBTS3TV=GS2.1.s1758699120$o12$g1$t1758699127$j53$l0$h0; _ga=GA1.1.152397546.1757152402"

}



# 获取第一层网址
def get_first_urls(first):
    page = requests.get(first,headers=headers).text
    urls = obj1.findall(page)
    return urls#返回第一层地址的一个列表
# 分别请求第二层网址拿到图片，写入文件
def get_imgs(third):
    third= third.replace('amp;','')
    img = requests.get(url=third,headers=headers)
    img_name = third.split('large/')[1]
    with open(r"C:\Users\admin\Desktop\tupian/" + f"{img_name}", "wb") as f:
        f.write(img.content)
    time.sleep(random.uniform(2,3))
    print(f"{img_name} saved")


#请求第一层网址，得到第二层网址的列表
def get_second_urls(second):
    urls = get_first_urls(second)
    lst = []
    for i in urls:
        i = requests.get(url=i,headers=headers).text
        img_urls = obj2.findall(i)
        lst.extend(img_urls)#得到第二层地址的列表
    with ThreadPoolExecutor(50) as executor:#多线程下载，用下载函数get_img
        for l in lst:
            executor.submit(get_imgs,l)

def remove_img():#删除不合要求的图片
    for a, b, c, in os.walk(r"C:\Users\admin\Desktop\tupian"):  # 三个参数返回路径，文件夹，文件
        for file in c:
            fsize = os.path.getsize(os.path.join(a, file))
            if fsize == 50 or fsize == 0:
                os.remove(os.path.join(a, file))




if __name__ == '__main__':
    for k in range(1,6):
        get_second_urls(f"https://moetu.club/category/pixiv/page/{k}")#开始下载5页资源
    remove_img()





















