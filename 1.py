import json

from selenium import webdriver
import re

def get_one_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver.page_source

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d*)</i>.*?data-src="(.*?)".*?'
                         'name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?'
                         'releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            '排名': item[0],
            '电影名': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5]+item[6],
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def main(offset: object) -> object:
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
