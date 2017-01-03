# -*- coding: utf-8 -*-


from SpiderPackage import SpiderClass,DownFiles
from UrlManager import UrlBox


def startSpider(pageUrlStr,startIndex,endIndex):
    pageBox = UrlBox.Box()
    for i in range(startIndex, endIndex):
        pageUrl = pageUrlStr % i
        pageBox.appendIntoBox(pageUrl)

    spider = SpiderClass.spider(pageBox)
    mp3Box, nameBox = spider.getMp3Box()
    DownFiles.downFiles(mp3Box, nameBox)



#主入口
if __name__=='__main__':
    '''
        breaking: http://www.dancering.cn/music_list-36-0-%d.html
        hiphop: http://www.dancering.cn/music_list-240-0-%d.html

    '''
    startSpider('http://www.dancering.cn/music_list-36-0-%d.html',1,81)




