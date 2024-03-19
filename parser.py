import datetime
import json
import random
import time
import asyncio
from bs4 import BeautifulSoup as bs
import requests as rq
from concurrent.futures import ThreadPoolExecutor
import re

import database
import functions


def get_headers():
    link = f'https://www.useragents.me/#most-common-desktop-useragents-json-csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    response = rq.get(link, headers=headers)
    soup = bs(response.text, 'lxml')
    res = soup.find_all('div', class_='table-responsive')[0].find_all('textarea')
    pattern = r'<textarea[^>]*>(.*?)<\/textarea>'
    ans = []
    for i in res:
        i = str(i)
        try:
            matches = re.findall(pattern, i)[0]
            ans.append(matches)
        except:
            continue

    return {'User-Agent': random.choice(ans)}


def parse_cards_links(country_abbreviations):
    res = set()
    time_start = datetime.datetime.now()
    for cat in range(0, 18):
        # print(f"category {cat}")
        for page in range(1, 9):
            headers = get_headers()
            for reg in country_abbreviations.values():
                print(f'parse page {page} country {reg} cat {cat}')
                # link = f'https://en.pinkoi.com/product/JdEZtNEK'
                # link = f'https://en.pinkoi.com/store/littlemountainslope?ref_sec=shop_info&amp;ref_created=1710601093&amp;ref_entity=item&amp;ref_entity_id=JdEZtNEK'
                link = f'https://en.pinkoi.com/browse?catp=group_{cat}&order=desc&sortby=created&shippable_geo={reg}&page={page}'
                response = rq.get(link, headers=headers)
                soup = bs(response.text, 'lxml')
                pattern = '<script type="application\/ld\+json">(.*?)<\/script>'
                matches = re.findall(pattern, str(soup))
                for m in matches:
                    m = json.loads(m)
                    if m['@type'] == 'Product':
                        res.add(m['offers']['seller']['url'])
    time_end = datetime.datetime.now()
    diff = time_end - time_start
    print(
        f'Время парсинга:{diff.total_seconds() / 60} минут\nСобрано {len(res)} карточек, из которых {len(set(res))} уникальных')
    #
    # # ТУТ Я ЗАПИСЫВАЮ ССЫЛКИ В ФАЙЛ
    # # ЭТО ТОЛЬКО ДЛЯ ТЕСТА, В ИДЕАЛЕ ССЫЛКИ ДОЖНЫ СРАЗУ ПОПАДАТЬ В ГЕТ СЕЛЛЕРС ФАЙЛ
    # #  with open('data/raw_data.txt', 'w', encoding='utf-8') as f:
    # #      f.write('\n'.join(list(set(res))))
    # #      f.close()
    return list(res)


# parse_cards_links(functions.country_abbreviations1)


# Я ЧИТАЮ ССЫЛКИ ИЗ ФАЙЛА ЧТОБЫ БЫЛО БЫСТРЕЕ!!!
# with open("data/raw_data.txt", "r", encoding="utf-8") as f:
#     content = f.read().split('\n')
# content = [x.strip('"') for x in content]

def get_sellers_file(country_abbreviations):
    data = parse_cards_links(country_abbreviations)
    ans = []
    shop_set = set()
    error_counter = 0
    t1 = datetime.datetime.now()
    for i in range(len(data)):
        try:
            headers = get_headers()
            response = rq.get(data[i], headers=headers)
            soup = bs(response.text, 'lxml')
            info = soup.find('div', class_='info-top')
            shop_name = info.find('h1').text
            country = info.find('div', class_='shop-info-list').find('div', class_='info').text
            reviews = info.find('span', class_='shop-rating__total').text[1:-1]
            online = info.find('div', class_='right-reply').find('div', class_='shop-info-table').find('div',
                                                                                                       class_='block').find(
                'div', class_='content').text
            try:
                reviews = int(reviews)
            except:
                reviews_int = ''
                for j in reviews:
                    if j.isdigit():
                        reviews_int += j
                reviews = int(reviews_int)
            if reviews < 10 and online == '1 day ago':
                answer = f'{reviews};{shop_name};{country};{online};{data[i]}'
                database.add_to_sellers(data[i], answer)
                print(answer)
                ans.append(answer)
        except Exception as e:
            print(f"A MISTAKE OCCURED: {e}")
            error_counter += 1
            continue
    t2 = datetime.datetime.now()
    diff = t2 - t1
    print(
        f'Время парсинга:{diff.total_seconds() / 60} минут\nОшибок возникло: {error_counter}\nСобрана инфа о {len(shop_set)} уникальных магазинах')
    return ans

# get_sellers_file(['https://en.pinkoi.com/store/yinke', 'https://en.pinkoi.com/store/exponent', 'https://en.pinkoi.com/store/goodviewvintageshop', 'https://en.pinkoi.com/store/xi-yao', 'https://en.pinkoi.com/store/tanluciana', 'https://en.pinkoi.com/store/queensybra-dress', 'https://en.pinkoi.com/store/jillpunk', 'https://en.pinkoi.com/store/klaraloveofficial', 'https://en.pinkoi.com/store/3twolight-vintage']
# )
