# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from UrlManager import UrlBox,NameBox

class spider:
    # 这里是街舞爱好者论坛Breaking音乐专区
    #breaking音乐：http://www.dancering.cn/music_list-36-0-1.html'
    #poppin音乐： http://www.dancering.cn/music_list-239-0-2.html
    def __init__(self,PageBox):
        self.PageBox=PageBox

    def getMp3Box(self):
        '''
        开始爬虫 分析以下：需要爬取得内容如下：
        1、music列表页
        2、通过每一个的数字aid从固定url返回值中获取对应aid
        3、url拼接得到需要的mp3的下载url

        4、真正花时间需要整理的其实就是最后第三步获取的url们
        :param index:
        :return:
        '''
        if not self.PageBox.isBoxEmpty():
            #如果传入的box不是空的那么就取出其中的URLList
            pageUrls=self.PageBox.getUrlList()

            #解析pageUrls并返回所有的aidUrls,而且获得nameBox
            aidBox,nameBox=spider.insertAidBox(self,pageUrls=pageUrls)
            aidUrls=aidBox.getUrlList()
            #解析aidUrls并返回mp3Urls
            mp3Box=spider.insertMp3Box(self,aidUrls=aidUrls)
            #比对一下MP3数量和名字数量
            if mp3Box.getBoxLength()==nameBox.getBoxLength():
                print('获取到Mp3数量为 %d' % mp3Box.getBoxLength())
                return mp3Box,nameBox
            else:
                return None
        else:
            print('传入的musicListPageUrls-Box是空的')
            return None

    def insertAidBox(self,pageUrls):
        '''
        通过处理传入的pageUrls获取对应的aidUrl和nameBox
        :param pageUrls:
        :return:
        '''
        # 把所有的获取aid的url加入到对应的box
        nameBox=NameBox.Box()
        aidBox = UrlBox.Box()
        for pageUrl in pageUrls:
            # print('总计抓取 %d 页数据，下面开始一页' % len(pageUrls))
            print('pageUrl是：  %s' % pageUrl)

            response = requests.get(pageUrl)
            if response.status_code == 200:
                # 请求返回成功
                soup = BeautifulSoup(response.text, 'html.parser')
                contentList = soup.find('div', 'bm_c xld')
                for item in contentList.findAll('li'):
                    aidContent = item.findAll('a')[0]['href']
                    aid = aidContent[(len(aidContent) - 6):len(aidContent)]  # 获取到数字形式的aid
                    aidUrl = 'http://www.dancering.cn/plugin.php?id=attachcenter:listening&aid=%s&infloat=yes&handlekey=music_action&inajax=1&ajaxtarget=fwin_content_music_action' % aid

                    aidName=item.findAll('a')[-1].text
                    nameBox.appendIntoBox(aidName)
                    aidBox.appendIntoBox(aidUrl)

                if nameBox.getBoxLength()==aidBox.getBoxLength():
                    print('aidBox和nameBox长度相等为：%d' % aidBox.getBoxLength())
                else:
                    print('注意！！！aid和name长度不相等，出现异常！！！')
            else:
                # 请求返回错误
                print('pageUrl返回错误，错误码：%d' % response.status_code)

        return aidBox,nameBox

    def insertMp3Box(self,aidUrls):
        mp3List=[]
        # 把所有的获取mp3的Url加入到对应的box
        mp3Box=UrlBox.Box()
        for aidUrl in aidUrls:
            responseAid = requests.get(aidUrl)
            #获取包含Aid的文本对象
            # print(responseTest.text)
            if responseAid.status_code == 200:
                realAid = re.findall(r'get_filecont\.php\?aid=(.*?)&loop', responseAid.text)[0]
                mp3Url = 'http://www.dancering.cn/source/module/forum/get_filecont.php?aid=%s' % realAid
                # print(mp3Url)
                mp3Box.appendIntoBox(mp3Url)
                print(mp3Url)
                print('获取到MP3链接URL：%d 个' % mp3Box.getBoxLength())
            else:
                print('aidUrl请求返回错误，错误码为： %d' %responseAid.status_code)
        return mp3Box



