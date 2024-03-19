import threading
import time

import parser as ps
import functions as fx
# def f1():
#     res = ps.parse_cards_links(fx.country_abbreviations1)
#     time.sleep(1)
#     with open('data/raw_data.txt', 'a', encoding='utf-8') as f:
#          f.write('\n'.join(res))
#          f.write('\n')
#          f.close()
#
# def f2():
#     res = ps.parse_cards_links(fx.country_abbreviations2)
#     time.sleep(1)
#     with open('data/raw_data.txt', 'a', encoding='utf-8') as f:
#          f.write('\n'.join(res))
#          f.write('\n')
#          f.close()
# def f3():
#     res = ps.parse_cards_links(fx.country_abbreviations3)
#     time.sleep(1)
#     with open('data/raw_data.txt', 'a', encoding='utf-8') as f:
#          f.write('\n'.join(res))
#          f.write('\n')
#          f.close()
# def f4():
#     res = ps.parse_cards_links(fx.country_abbreviations4)
#     time.sleep(1)
#     with open('data/raw_data.txt', 'a', encoding='utf-8') as f:
#          f.write('\n'.join(res))
#          f.write('\n')
#          f.close()
with open("data/raw_data.txt", "r", encoding="utf-8") as f:
    content = f.read().split('\n')

content = fx.split_list_into_four_parts(content)

def f1(content):
    ans = ps.get_sellers_file(content)
    time.sleep(1)
    with open("data/data.txt", "a", encoding="utf-8") as f:
        content = '\n'.join(ans)
        f.write(content)
        f.write('\n')
        f.close()
def f2(content):
    ans = ps.get_sellers_file(content)
    time.sleep(1)
    with open("data/data.txt", "a", encoding="utf-8") as f:
        content = '\n'.join(ans)
        f.write(content)
        f.write('\n')
        f.close()

def f3(content):
    ans = ps.get_sellers_file(content)
    time.sleep(1)
    with open("data/data.txt", "a", encoding="utf-8") as f:
        content = '\n'.join(ans)
        f.write(content)
        f.write('\n')
        f.close()
def f4(content):
    ans = ps.get_sellers_file(content)
    time.sleep(1)
    with open("data/data.txt", "a", encoding="utf-8") as f:
        content = '\n'.join(ans)
        f.write(content)
        f.write('\n')
        f.close()

# thread1 = threading.Thread(target=f1)
# thread2 = threading.Thread(target=f2)
# thread3 = threading.Thread(target=f3)
# thread4 = threading.Thread(target=f4)

thread1 = threading.Thread(target=f1, args=(content[0],))
thread2 = threading.Thread(target=f2, args=(content[1],))
thread3 = threading.Thread(target=f3, args=(content[2],))
thread4 = threading.Thread(target=f4, args=(content[3],))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

# fx.remove_duplicate_lines("data/raw_data.txt")
# fx.count_unique_lines("data/raw_data.txt")
