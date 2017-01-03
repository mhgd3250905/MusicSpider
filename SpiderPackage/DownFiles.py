# -*- coding: utf-8 -*-

import threading
import requests
from contextlib import closing
import re
import sys
#线程



class myThread(threading.Thread):

    def __init__(self, name,spiderClass):
        threading.Thread.__init__(self)
        self.name = name
        self.spiderClass= spiderClass

    def run(self):
        print("开始线程：" + self.name)
        self.spiderClass.downLoad()
        print("退出线程：" + self.name)


# 作者：微微寒
# 链接：https://www.zhihu.com/question/41132103/answer/93438156
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)




class Down():
    def __init__(self,urls,names):
        self.urls=urls
        self.names=names

    def downLoad(self):


        # for i,url in enumerate(self.urls):
        #     name=re.sub(r'[\\\/\:\*\?\"\<\>\|\.\~]', "", self.names[i])
        #     print('即将下载文件%s' % name)
        #     responseMp3 = requests.get(url)
        #     if responseMp3.status_code == 200:
        #         with open("%s.mp3" % name, "wb") as code:
        #             code.write(responseMp3.content)
        #             print("下载完成")
        # for i,url in enumerate(self.urls):
        #
        #     name = re.sub(r'[\\\/\:\*\?\"\<\>\|\.\~]', "", self.names[i])
        #     # print('即将下载文件%s' % name)
        #     responseMp3 = requests.get(url,stream=True)
        #     with closing(responseMp3) as response:
        #         chunk_size = 512  # 单次请求最大值
        #         content_size = int(response.headers['content-length'])  # 内容体总大小
        #         print(content_size)
        #         progress = ProgressBar(name, total=content_size,
        #                                unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        #         with open("F:\街舞爱好者爬虫音乐\HiphopMusic\%s.mp3" % name, "wb") as file:
        #             for data in response.iter_content(chunk_size=chunk_size):
        #                 file.write(data)
        #                 progress.refresh(count=len(data))

            for i, url in enumerate(self.urls):
                name = re.sub(r'[\\\/\:\*\?\"\<\>\|\.\~]', "", self.names[i])
                print('')
                print('即将下载文件%s' % name)
                responseMp3 = requests.get(url, stream=True)
                total_length = int(responseMp3.headers['content-length'])  # 内容体总大小
                with open("%s.mp3" % name, "wb") as code:

                    if total_length is None:  # no content length header
                        code.write(responseMp3.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in responseMp3.iter_content(chunk_size=1024):
                            dl += len(data)
                            code.write(data)
                            done = int(50 * dl / total_length)
                            sys.stdout.write("\r[%s%s]" % ('█' * done, ' ' * (50 - done)))
                            sys.stdout.flush()

                        print('')
                        print('下载完成：%s' % name)



def downFiles(mp3Box,nameBox):
    '''
    1 统计数量
    2 按照数量分配线程：这里默认设置一个线程下载100首歌好了
    3 开启所有线程然后下载
    4 关闭所有线程
    :param mp3Urls:
    :return:
    '''
    nameList=nameBox.getNameList()
    mp3Urls=mp3Box.getUrlList()
    #再一次验证一下我们的名字和MP3数量是否对应
    if nameBox.getBoxLength()!=mp3Box.getBoxLength():
        exit()
    mp3Length=mp3Box.getBoxLength()

    threadList=[]
    #初始化线程List
    #分隔list

    for i in range(0, mp3Length, 100):
        mp3UrlsTemp=[]
        namesTemp=[]
        mp3UrlsTemp = mp3Urls[i:i + 100]
        namesTemp=nameList[i:i + 100]
        downTemp=Down(mp3UrlsTemp,namesTemp)
        thread=myThread('音乐下载',downTemp)
        threadList.append(thread)


    if len(threadList)>0:
        print('线程分配完毕，即将开启线程数为：%d' % len(threadList))
    else:
        exit()

    for threadItem in threadList:
        threadItem.start()

    for threadItem in threadList:
        threadItem.join()

    print('')






