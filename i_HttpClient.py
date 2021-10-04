import gzip
import http.client
import os
import re

from io import BytesIO
from urllib.request import urlretrieve


class i_HttpClient:
    def __init__(self, cookie):
        """
        :param cookie:
        :type cookie: str
        """
        # link: 链接去重
        self.link = set()
        # downCount: 下载页面计数
        self.downCount = 0
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
        conn = http.client.HTTPSConnection("www.ireader.com")
        conn.request("GET", "/index.php?ca=Chapter.Content&bid=" + bid + "&cid=" + cid, headers=self.headers)
        page = conn.getresponse()
        data = page.read()
        buff = BytesIO(data)
        f = gzip.GzipFile(fileobj=buff)
        page = f.read().decode('utf-8')

        if page != '' and page != "Array":
            if not os.path.isdir('./books/' + bid):
                os.makedirs('./books/' + bid)
            img_url = re.findall(r'http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[s|g](?=\?v=)', page)
            for i in img_url:
                page = page.replace(i, re.split('/', i)[-1])
                self.link.add(i)
            with open('./books/' + bid + '/' + bid + '_' + cid + '.html', 'w', encoding='utf-8') as f:
                f.write(page)
                self.downCount += 1
                print(".", end="")
            self.get_page(bid, str(1 + int(cid)))
        else:
            self.down_url(bid)
            print("总下载" + str(self.downCount) + "个页面 ✔")

    def down_url(self, bid):
        for i in self.link:
            urlretrieve(i, './books/' + bid + '/' + re.split('/', i)[-1])
            self.downCount += 1
            print(".", end="")


if __name__ == '__main__':
    cookie = 'pc_yz_ireader_zypc_guid=c00eAgBUVlZWBwYJUgtYAwNQUVxTVwACUV0EAgYVW1ECChQEBCVVXiN2dRQgAVckTFdwfQ5PC3dzUhkFA19RJHd0dwp1UCdEXQ; ' \
             'pc_yz_ireader_userInfo=f373CAVSAwNSAVYCUlYGBlJVCAAHBlFWAAQBVlUDWwFcTBYCDVgRRhFUFHwDXgZADUMDBQEKRwwDU1ULD1tRBF8ARwNGWAIBWBMUVwVaEBZTQm1NQFVHXkNcUgkUVUMIGw; ' \
             'Hm_lvt_2583df02aa8541db9378beae2ed00ba0=1616294763,1616809801,1617438869,1618623411; ' \
             'ZyId=51e9d143607a3bab47eeb'
    page = i_HttpClient(cookie)
    book_list = [12492459]
    for i in book_list:
        print("start Down " + str(i), end="📥")
        page.get_page(bid=str(i), cid="1")
        print("---" * 9)
