import requests
from multiprocessing import Pool
import os, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from retrying import retry

'''
 原理就是把所有的小片段拼接成一部电影
 通过视频解析网站:http://v.laod.cn/ 将视频解析成小文件
 获取小文件的url，通过此程序将所有小文件下载到本地
 win命令:copy /b *ts abc.mp4,作用:将所有的小文件组合成一个整体
'''

@retry(stop_max_attempt_number=3)
def templ(n):
    # 例:取腾讯某电影的url，到vip解析网站解析成小文件，第一个小文件的url如下
    # url = "https://videos4.jsyunbf.com/2019/01/10/tBku9gSXlALabLUH/out%s.ts"% n
    url = "https://135zyv6.xw0371.com/2019/02/07/cTJrO8R0uALqvMCD/out%s.ts"% n
    print("正在下载 %s . . . \n " % url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }

    r = requests.get(url, headers=headers, verify=False, timeout=20)  # verify无需证书验证
    f = open('./mp4/{}'.format(url[-10:]), 'ab')
    f.write(r.content)
    f.close()


# 调用系统命令 cat 合并 ts文件
def merge():
    # os.popen('ping www.baidu.com -c 3').readlines()
    os.popen('cat ./mp4/out%s.ts >> ./mp4/merge.ts' % num)


if __name__ == '__main__':
    pool = Pool(20)  # 创建20个进程去运行，并发
    for I in range(1, 1332):  # 最多需要多少个片段，将视频拉到最后，在审查元素中就会显示
        num = "%03d" % I
        # print(num)
        pool.apply_async(templ(num))  # 创建进程，任务名:temp1
        #merge()

    pool.close()
    pool.join()
'''
 打印 001 的两种方式 : for I in range(1,120):print("%03d"%I)
 					 for I in range(1,123):print(str(I).zfill(3))
'''