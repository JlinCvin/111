import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlencode
from pyquery import PyQuery as pq

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie':'SUID=5700ECB7572B8B0A5BE9A7410006D06D; wuid=AAGmR1O/IwAAAAqLK1ePpQ0AGwY=; CXID=4911FE248F6B3FA7A0C112FE82BE2917; ad=1yllllllll2bfzNxlllllVsII19lllllnhXDMyllll9lllllRVxlw@@@@@@@@@@@; sw_uuid=3430244114; sg_uuid=1094690956; ssuid=9274323000; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; IPLOC=CN4401; SUV=00D80F4D3B29FCE35BF6B0358AA5C660; ABTEST=0|1543631414|v1; SNUID=F8A44813A3A1D848168259D9A4E875A1; weixinIndexVisited=1; sct=1; JSESSIONID=aaa-QB2DXHzBvayoLE6Cw; ppinf=5|1543631618|1544841218|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlOTglQkIlRTUlOTglQkIlRTUlOTglQkJ8Y3J0OjEwOjE1NDM2MzE2MTh8cmVmbmljazoyNzolRTUlOTglQkIlRTUlOTglQkIlRTUlOTglQkJ8dXNlcmlkOjQ0Om85dDJsdUJKWHd1SlFTVnZWTDVzR2ZBbFZvTE1Ad2VpeGluLnNvaHUuY29tfA; pprdig=QZLSLVsr1cib2yWCezP_WaFb7Q3KokrvbWw1mFW5od1lvZD9f_JqyJbmDe_mnRECmyLd7ny51jR_Ma3yegsRWhcFIHP4qvqtnPbYkv2fT0MDxg63oXOzTjmvRKBI6DtGhGGwtsbuf1uo9ucSJTT70hFD6LdWbLYRi8_2_RMJ3dE; sgid=01-23067290-AVwB8wIrHQjrbcPZUGPPrKE; ppmdig=15436316180000008f608dbe09b59d6feafb7a9a37f999e5'
    'Host:weixin.sogou.com'
    'Upgrade-Insecure-Requests:1'
    'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
}

keyword = '风景'
proxy_pool_url = 'http://127.0.0.1:5000/get'

proxy = None
max_count = 5

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('crewing', url)
    print('Trying count', count)
    global proxy
    if count >= max_count:
        print('Tried Too many counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('using proxy', proxy)
                count += 1
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)

def get_index(keyword,page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page,
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_datail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_datail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    data = doc('#publish_time').text()
    nickname = doc('.rich_media_meta_list .rich_media_meta_nickname').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title' : title,
        'content' : content,
        'data' : data,
        'nickname' : nickname,
        'wechat' : wechat,
    }

def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_datail(article_url)
                if article_html:
                    article_data = parse_datail(article_html)
                    print(article_data)

if __name__ == '__main__':
    main()