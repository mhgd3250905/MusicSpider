# -*- coding: utf-8 -*-

class Box:
    '''
        这里设置一个UrlBox
        因为所有的一个Box对应一个线程
        前方爬虫将所有的需要下载的URL放置到Box中
        所以每次使用的时候是有需要爬取的Url
        那么我们新建一个Box，将URL装进去
        如果box空了那么就关闭对应的线程
    '''

    def __init__(self):
        self.urlList=[]

    #获取UrlBox里面是否还有链接：如果有返回True/如果没有返回False
    def isBoxEmpty(self):
        '''
        box是否是空的，如果是空的那么线程就可以结束了
        :return: 是否是空的
        '''
        if len(self.urlList)>0 :
            return False
        elif len(self.urlList)==0:
            return True

    def getUrlList(self):
        '''
        获取box中的List
        :return: urlList
        '''
        if Box.getBoxLength(self)>0:
            return self.urlList

    def getBoxLength(self):
        '''
        返回box的size
        :return: box目前的容量
        '''
        return len(self.urlList)

    #向urlBox中添加URL
    def appendIntoBox(self,url):
        '''
        当box没有满载的时候就可以把url加入进来
        :param url:
        :return: 是否加入成功
        '''
        self.urlList.append(url)
        return True




