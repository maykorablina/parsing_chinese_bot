import datetime
import random
import time
import asyncio
from bs4 import BeautifulSoup as bs
import requests as rq
from concurrent.futures import ThreadPoolExecutor
import re

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

def parse_cards_links():
    country_abbreviations = {
        "Japan": "JP",
        "United Kingdom": "GB",
        "Taiwan": "TW",
        "Hong Kong": "HK",
        "Macau": "MO",
        "Singapore": "SG",
        "Mainland China": "CN",
        "Malaysia": "MY",
        "Thailand": "TH",
        "United States": "US",
        "Australia": "AU",
        "Canada": "CA",
        "Germany": "DE",
        "Republic of Korea": "KR",
        "France": "FR",
        "Vietnam": "VN",
        "Philippines": "PH",
        "Indonesia": "ID",
        "Norway": "NO",
        "Italy": "IT",
        "Netherlands": "NL",
        "Austria": "AT",
        "Belgium": "BE",
        "Spain": "ES",
        "Denmark": "DK",
        "Czechia": "CZ",
        "Greece": "GR",
        "Switzerland": "CH",
        "Ireland": "IE",
        "India": "IN",
        "Israel": "IL",
        "Hungary": "HU",
        "Finland": "FI",
        "Lithuania": "LT",
        "Bulgaria": "BG",
        "Portugal": "PT",
        "Estonia": "EE",
        "Latvia": "LV",
        "Belarus": "BY",
        "Sweden": "SE",
        "Turkey": "TR",
        "Poland": "PL",
        "United Arab Emirates": "AE",
        "Luxembourg": "LU",
        "New Zealand": "NZ",
        "Romania": "RO",
        "Slovakia": "SK",
        "Slovenia": "SI",
        "Saudi Arabia": "SA",
        "Cambodia": "KH",
        "Russia": "RU",
        "Malta": "MT",
        "Sri Lanka": "LK",
        "Cyprus": "CY",
        "Iceland": "IS",
        "Croatia": "HR",
        "Moldova": "MD",
        "Kazakhstan": "KZ",
        "Armenia": "AM",
        "Qatar": "QA",
        "Bahrain": "BH",
        "Kuwait": "KW",
        "Azerbaijan": "AZ",
        "Uzbekistan": "UZ",
        "Oman": "OM",
        "Jordan": "JO",
        "Iran": "IR",
        "Pakistan": "PK"}
    res = []
    time_start = datetime.datetime.now()
    for cat in range(0, 18):
        # print(f"category {cat}")
        for page in range(1, 4):
            headers = get_headers()
            for reg in country_abbreviations.values():
                print(f'parse page {page} country {reg} cat {cat}')
                # link = f'https://en.pinkoi.com/product/JdEZtNEK'
                # link = f'https://en.pinkoi.com/store/littlemountainslope?ref_sec=shop_info&amp;ref_created=1710601093&amp;ref_entity=item&amp;ref_entity_id=JdEZtNEK'
                link = f'https://en.pinkoi.com/browse?catp=group_{cat}&order=desc&sortby=created&shippable_geo={reg}&page={page}'
                response = rq.get(link, headers=headers)
                soup = bs(response.text, 'lxml')
                # pattern = '<script type="application\/ld\+json">(.*?)<\/script>'
                # matches = re.findall(pattern, str(soup))
                # print(matches)
                # soup.find_all()
                # print(str(soup))
                # time.sleep(60)
                pattern = r'"https://en.pinkoi.com/product/[A-Za-z0-9]+"'
                matches = re.findall(pattern, str(soup))
                res += matches
    time_end = datetime.datetime.now()
    diff = time_end - time_start
    print(f'Время парсинга:{diff.total_seconds() / 60} минут\nСобрано {len(res)} карточек, из которых {len(set(res))} уникальных')

   # ТУТ Я ЗАПИСЫВАЮ ССЫЛКИ В ФАЙЛ
   # ЭТО ТОЛЬКО ДЛЯ ТЕСТА, В ИДЕАЛЕ ССЫЛКИ ДОЖНЫ СРАЗУ ПОПАДАТЬ В ГЕТ СЕЛЛЕРС ФАЙЛ
   #  with open('data/raw_data.txt', 'w', encoding='utf-8') as f:
   #      f.write('\n'.join(list(set(res))))
   #      f.close()
    return list(set(res))

# Я ЧИТАЮ ССЫЛКИ ИЗ ФАЙЛА ЧТОБЫ БЫЛО БЫСТРЕЕ!!!
# with open("data/raw_data.txt", "r", encoding="utf-8") as f:
#     content = f.read().split('\n')
# content = [x.strip('"') for x in content]

def get_sellers_file(data):
    ans = []
    shop_set = set()
    error_counter = 0
    t1 = datetime.datetime.now()
    for i in range(len(data)):
        try:
            data[i] = data[i].strip('"')
            headers = get_headers()
            response = rq.get(data[i], headers=headers)
            soup = bs(response.text, 'lxml')
            res = soup.find('div', class_='m-product-shop m-box js-block-shop')
            shop_counry = res.find('div', class_='shop-country').text.strip()
            shop_info = res.find('div', class_='shop_info')
            shop_name = shop_info.find('div',class_='shop-name').text.strip()

            if shop_name in shop_set:
                continue
            shop_set.add(shop_name)
            n_revs = shop_info.find_all('div', class_='m-review-info__total')
            online = res.find('dl',class_='m-product-list').find('dd').text.strip()
            if n_revs:
                n_revs = n_revs[0].text[1:-1]
            else:
                n_revs=0
            answer = f'{n_revs};{shop_name};{shop_counry};{online};{data[i]}'
            # print("from part 1")
            print(answer)
            ans.append(answer)
        except Exception as e:
            print(f"A MISTAKE OCCURED: {e}")
            error_counter += 1
            continue
    t2 = datetime.datetime.now()
    diff = t2 - t1
    print(f'Время парсинга:{diff.total_seconds() / 60} минут\nОшибок возникло: {error_counter}\nСобрана инфа о {len(shop_set)} уникальных магазинах')
    with open("data/data.txt", "w", encoding="utf-8") as f:
        content = '\n'.join(ans)
        f.write(content)
        f.close()
    return content

# get_sellers_file(content)




