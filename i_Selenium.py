import os
import re
from typing import List
from urllib.request import urlretrieve

from selenium import webdriver


class i_Selenium:
    def __init__(self):
        self.__url = "http://www.ireader.com/index.php"
        self.__drop = webdriver.Edge()
        self.__drop.get(self.__url)
        self.__drop.implicitly_wait(5)

    def add_cookies(self, __cookies):
        """
        对于需要权限的书籍，添加自己账号的cookies
        :param __cookies:
        :type __cookies: List
        :return:
        """
        for cookie in __cookies:
            self.__drop.add_cookie(cookie_dict=cookie)
        self.__drop.refresh()

        # 验证登录状态
        if len(self.__drop.find_elements_by_xpath("//div[@id='login_box']//i[not(text())]")) == 0:
            print("登录成功\n开始下载")
        else:
            self.__drop.quit()
            print("Cookies登录失败，已退出")

    def quit(self):
        """
        结束进程
        :return:
        """
        self.__drop.quit()

    @staticmethod
    def __down_link(bid, link):
        """
        下载外链
        :param bid: 图书Id
        :type bid: str
        :param link: 外链集合
        :type link: set
        :return:
        """
        for i in link:
            urlretrieve(i, './books/' + bid + '/' + re.split('/', i)[-1])

    def get_books(self, bid, cid):
        """
        获取电子书的网页源码
        :param bid: 图书ID
        :type bid: str
        :param cid: 章节ID
        :type cid: str
        :return:
        """
        cidx = cid
        link = set()
        # 搞个目录存文件
        if not os.path.isdir('./books/' + bid):
            os.makedirs('./books/' + bid)

        self.__drop.get("http://www.ireader.com/index.php?ca=Chapter.Index&bid=" + bid + "&cid=" + cid)

        # 循环下一章节，直至结束
        while cid == cidx:
            self.__drop.switch_to.frame("iframe_chapter")
            __page = self.__drop.page_source

            # 获取并替换书中外链
            img_url = re.findall(r'http.*(?=\?v=)', __page)
            for i in img_url:
                __page = __page.replace(i, re.split('/', i)[-1])
                link.add(i)
            # 保存html文件
            with open('./books/' + bid + '/' + bid + '_' + cid + '.html', 'a', encoding='utf-8') as f:
                f.write(__page)

            self.__drop.switch_to.default_content()
            self.__drop.find_element_by_xpath("//s[@class='read_s down']").click()
            cid = str(1 + int(cid))
            cidx = self.__drop.current_url.split("&cid=")[1]

        self.__down_link(bid, link)


if __name__ == '__main__':
    cookies = [{'name': 'ZyId', 'value': '***', 'domain': '.ireader.com'},
               {'name': 'pc_yz_ireader_zypc_guid',
                'value': '***',
                'domain': '.ireader.com'},
               {'name': 'pc_yz_ireader_userInfo',
                'value': '***',
                'domain': '.ireader.com'}]
    page = i_Selenium()
    page.add_cookies(cookies)
    page.get_books("12340946", "1")
    page.quit()
