import json

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from multiprocessing import Pool
import time


def get_one_page(url, headers):
    try:

        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None


def parse_one_page(html):
    bs_obj = BeautifulSoup(html)
    items = bs_obj.find_all("dd")
    for item in items:
        yield {
            'img': item.find('img', {'class': 'board-img'}).get('data-src'),
            'title': item.find('p', {'class': 'name'}).find('a').get('title').strip(),
            'stars': item.find('p', {'class': 'star'}).text.strip(),
            'time': item.find('p', {'class': 'releasetime'}).text.strip(),
            'score': item.find('i', {'class': 'integer'}).text + item.find('i', {'class': 'fraction'}).text
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }
    url = 'https://maoyan.com/board/4?offset=' + str(offset)

    html = get_one_page(url, headers)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
    # time.sleep(1)

if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    #     time.sleep(1)
    # 使用多进程
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
