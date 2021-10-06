import gzip, http.client, json, os, re
from io import BytesIO
from urllib.request import urlretrieve


class IHttpClient:
    def __init__(self, _cookie):
        """
        :param _cookie:
        :type _cookie: str
        """
        # link: 链接去重
        self.link = set()
        # downCount: 下载页面计数
        self.downCount = 0
        self.headers = {
            'Content-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': _cookie,
            'Host': 'www.ireader.com.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.ireader.com/index.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
        }

    def get_page(self, bid: str, cid: str):
        """
        下载书籍章节
        :param bid: 掌阅书号
        :param cid: 章节号
        :return:
        """
        total_page = self.get_total_page(bid)
        conn = http.client.HTTPSConnection("www.ireader.com.cn")
        conn.request("GET", "/index.php?ca=Chapter.Content&bid=" + bid + "&cid=" + cid, headers=self.headers)
        __page = conn.getresponse()
        data = __page.read()
        buff = BytesIO(data)
        f = gzip.GzipFile(fileobj=buff)
        __page = f.read().decode('utf-8')

        if __page != '' and __page != "Array" and int(cid) < total_page:
            if not os.path.isdir('./books/' + bid):
                os.makedirs('./books/' + bid)
            img_url = re.findall(r'http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[s|g](?=\?v=)', __page)
            for _i_ in img_url:
                __page = __page.replace(_i_, re.split('/', _i_)[-1])
                self.link.add(_i_)
            with open('./books/' + bid + '/' + bid + '_' + cid + '.html', 'w', encoding='utf-8') as f:
                f.write(__page)
                self.downCount += 1
                print(".", end="")
                if int(cid) % 100 == 0: print()
            self.get_page(bid, str(1 + int(cid)))
        else:
            print("已下载 " + str(self.downCount) + " 个页面 ✔")
            self.down_url(bid)
            print("总下载 " + str(self.downCount) + " 个页面 ✔")

    def down_url(self, bid: str):
        # 按照文件名进一步去重
        dict_link = {}
        for _i_ in self.link:
            dict_link[re.split('/', _i_)[-1]] = _i_

        for _k, _v in dict_link.items():
            urlretrieve(_v, './books/' + bid + '/' + _k)
            print(_v)
            self.downCount += 1

    def get_total_page(self, bid: str) -> int:
        """
        获取书籍最后一章的ID
        :param bid: 掌阅书号
        :return: 最后一章的号码
        """
        conn = http.client.HTTPSConnection("www.ireader.com.cn")
        conn.request("GET", "/index.php?ca=Chapter.List&ajax=1&bid=" + bid + "&__page=1&pageSize=1",
                     headers=self.headers)
        __page = conn.getresponse()
        __page = gzip.GzipFile(fileobj=BytesIO(__page.read())).read().decode("utf-8")
        return json.loads(__page)["page"]["total"]


if __name__ == '__main__':
    cookie = ""
    page = IHttpClient(cookie)
    book_list = [12129841]
    for i in book_list:
        print("start Down " + str(i), end=" 📥\n")
        page.get_page(bid=str(i), cid="1")
