import os
import re
from urllib.request import urlretrieve

import requests


class i_Requests:
    def __init__(self, cookie):
        """
        :param cookie:
        :type cookie: str
        """
        self.headers = {
            'Content-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': cookie,
            'Host': 'www.ireader.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.ireader.com/index.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
        }

    def get_page(self, bid, cid):
        """
        :param bid: 图书ID
        :type bid: str
        :param cid: 章节ID
        :type cid: str
        :return:
        """
        url = "http://www.ireader.com/index.php?ca=Chapter.Content&pca=bookdetail.index&bid=" + bid + "&cid=" + cid
        response = requests.request("GET", url, headers=self.headers)
        response.encoding = 'utf8'
        page = response.text
        link = set()

        if page != '' and page != "Array":
            if not os.path.isdir('./books/' + bid):
                os.makedirs('./books/' + bid)
            img_url = re.findall(r'http.*(?=\?v=)', page)
            for i in img_url:
                page = page.replace(i, re.split('/', i)[-1])
                link.add(i)
            with open('./books/' + bid + '/' + bid + '_' + cid + '.html', 'a', encoding='utf-8') as f:
                f.write(page)
            self.get_page(bid, str(1 + int(cid)))
        for i in link:
            urlretrieve(i, './books/' + bid + '/' + re.split('/', i)[-1])
