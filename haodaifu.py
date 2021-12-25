import requests
import re

"""
爬虫 + 正则表达式的一个例子：爬取好大夫网站中的儿科学每一种疾病对应的网址。
Points:
1. 使用requests如果不指定headers，有可能返回403错误（一般是爬虫被网站发现而禁止了）
2. 正则表达式的捕获语法：(?<name>exp)
3. 正则表达式的使用实例：compile / search / group 
"""

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

r = requests.get("https://www.haodf.com/jibing/xiaoerke/list.htm", headers=headers)
if r.status_code != 200:
    raise RuntimeError("Status code is {0}".format(r.status_code))

pattern = '<a href="(?P<first>[/a-z.]+)" target=.*>(?P<last>\\w+)</a>'
regx = re.compile(pattern)

result = {}
for line in r.text.split('\n'):
    m = regx.search(line)
    if m:
        result[m.group(2)] = "https://www.haodf.com" + m.group(1)

for key in sorted(result):
    print("{0}:\t{1}".format(key, result[key]))
