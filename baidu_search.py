# coding=utf-8
import random
import requests
import time
import re
import string

proxys = [
    '221.130.192.237:80',
    '61.179.129.249:80',
    '123.126.158.50:80',
]

proxy = {
    'http': '140.249.88.250:80',
}

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/76.0.3809.100 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0"
]

referer_list = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.yahoo.com/',
    'https://www.amazon.com/',
    'https://www.facebook.com/',
    'https://www.twitter.com/',
    'https://www.instagram.com/',
    'https://www.linkedin.com/',
    'https://github.com/',
    'https://www.reddit.com/',
    'https://www.quora.com/',
    'https://www.wikipedia.org/',
    'https://www.stackoverflow.com/',
    'https://news.ycombinator.com/',
    'https://www.ebay.com/',
    'https://www.pinterest.com/',
    'https://www.apple.com/',
    'https://www.microsoft.com/',
    'https://www.netflix.com/',
    'https://www.nytimes.com/',
    'https://www.cnn.com/',
    'https://www.bbc.com/',
    'https://www.walmart.com/',
    # 可以根据需要添加更多的 Referer
]


def generate_random_cookie():
    cookie_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    cookie_value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return f"{cookie_name}={cookie_value}"


selected_referer = random.choice(referer_list)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': '; '.join([generate_random_cookie() for _ in range(3)]),
    'Referer': selected_referer,
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_url(url: str) -> str:
    try:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 302 and 'Location' in r.headers.keys():
            return r.headers['Location']
    except Exception:
        pass
    return ''


def get_search_num(keyword: str, starttime: int, endtime: int, domain: str = None):
    keyword = 'site: {} {}'.format(domain, keyword) if domain else keyword
    params = (
        ("rtt", "1"),
        ("bsst", "1"),
        ("cl", "2"),
        ("tn", "news"),
        ("ie", "utf-8"),
        ("word", keyword),
        ('rsv_pq', '9a80a6af00087e89'),
        ('rsv_t', '589fNQLugE82M0x4qNc9KvI6pZRsjQoKJnkprjPffd2Us9wxtoIf35DpbLs'),
        ("rqlang", "cn"),
        ("rsv_enter", "1"),
        ("rsv_dl", "tb"),
        ('gpc', 'stf={},{}|stftype=2'.format(starttime, endtime)),
        ("tfflag", "1")
    )
    while True:
        try:
            response = requests.get('https://www.baidu.com/s', headers=headers, params=params, timeout=5, proxies=proxy)
            reg = '>百度为您找到相关资讯(.*?)个'
            findlist = re.findall(reg, str(response.text))
            nums = findlist[0].replace('约', '').replace(',', '')
            print('nums:{}'.format(nums))
            time.sleep(10)
            break
        except Exception as e:
            print("errors:{}".format(str(e)))
            headers['User-Agent'] = user_agents[random.randint(0, len(user_agents) - 1)]
            proxy['http'] = proxys[random.randint(0, len(proxys) - 1)]
            time.sleep(3)
    return nums
