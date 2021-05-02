import gzip
import http.client
import json
from io import BytesIO

headers = {
    'Content-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Host': 'www.ireader.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ireader.com/index.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
}

bid = "12042183"

conn = http.client.HTTPSConnection("www.ireader.com")
conn.request("GET", '/index.php?ca=Chapter.List&ajax=1&bid=' + bid + '&pageSize=1000', headers=headers)
page = conn.getresponse()
data = page.read()
buff = BytesIO(data)
f = gzip.GzipFile(fileobj=buff)
page = f.read().decode('utf8')
pl = json.loads(page)

print("""
---
title: """ + bid + """
copyright: false
---

---

<div style="padding: 1em;margin: 1em 1em;border-bottom: dashed;border: 2px solid;border-radius: 25px;">
<iframe name="ireader" height=560 width=100%
src="/memo/books/book/""" + bid + """/""" + bid + """_1.html"
frameborder=0
allowfullscreen>
</iframe></div>

<div class="φgc">
""", end="")

for i in pl['list']:
    print('<is-m class="φep"><a title="字数=', end='')
    print(str(i['wordCount']) + '" onClick="a(\'' + str(i['id']), end="")
    print('\')" class="φeq φn φp">' + i['chapterName'], end="")
    print('</a></is-m>')

print("""</div>

<script>
    function a(cid) {
        window.frames["ireader"].location.href = "/memo/books/book/""" + bid + """/""" + bid + """_" + cid + ".html"
    }
</script>
<style>
.φg a:hover {color: rgb(255,165,2);}
</style>
""")
