import threading
import time
import parser as ps
import functions as fx

lock = threading.Lock()

def write_to_file(data):
    with lock:
        with open("data.txt", "a", encoding="utf-8") as f:
            content = '\n'.join(data)
            f.write(content)
            f.write('\n')

def get_sellers_data(country_abbreviations):
    ans = ps.get_sellers_file(country_abbreviations)
    write_to_file(ans)

threads = []
for abbreviations in [fx.country_abbreviations1, fx.country_abbreviations2, fx.country_abbreviations3, fx.country_abbreviations4]:
    thread = threading.Thread(target=get_sellers_data, args=(abbreviations,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Все потоки успешно завершили свою работу.")


