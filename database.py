import sqlite3
import datetime
from functions import PAYMENT_PERIOD
conn = sqlite3.connect('bot.db')

# c = conn.cursor()
#
# c.execute('''CREATE TABLE IF NOT EXISTS users
#              (id INT UNSIGNED PRIMARY KEY,
#               is_paid BOOLEAN,
#               is_admin BOOLEAN,
#               pay_time DATETIME,
#               last_login DATETIME,
#               last_page INT UNSIGNED)''')
#
#
#
# c.execute('''CREATE TABLE IF NOT EXISTS sellers
#     (id INT PRIMARY KEY,
#     description VARCHAR(1000),
#     is_sent BOOLEAN)''')
# #
# conn.commit()
# conn.close()



def clear_table(table):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table}')
    conn.commit()
    conn.close()

def reset_data(data):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    data_to_insert = []
    for d in range(len(data)):
        data_to_insert.append((d, data[d], False))
    cursor.execute('DELETE FROM sellers')
    conn.commit()
    cursor.executemany('INSERT INTO sellers (id, description, is_sent) VALUES (?, ?, ?)', data_to_insert)
    conn.commit()
    conn.close()

def drop_table(table):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute(f'DROP TABLE {table}')
    conn.commit()
    conn.close()

def select_by_id(table, id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (id,))
    ans = cursor.fetchone()
    # print(ans)
    conn.close()
    return ans

def select_all(table):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    ans = cursor.fetchall()
    conn.close()
    return ans

def select_and_delete():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM sellers WHERE is_sent = 0;")
    good = cursor.fetchone()
    if not good:
        conn.commit()
        conn.close()
        print("записи в таблице закончились")
        return False
    cursor.execute("UPDATE sellers SET is_sent = ? WHERE id = ?", (1, good[0]))
    conn.commit()
    conn.close()
    return good



def update_page(change, id, default=False):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    if default:
        cursor.execute("UPDATE users SET last_page = ? WHERE id = ?", (0, id))
        conn.commit()
        conn.close()
        return 0
    else:
        cur_page = select_by_id('users', id)[-1]
        # print(cur_page)
        cur_page += change
        cursor.execute("UPDATE users SET last_page = ? WHERE id = ?", (cur_page, id))
        conn.commit()
        conn.close()
        return cur_page

def n_sellers():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sellers")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def user_logged(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    new_last_login = datetime.datetime.now().replace(microsecond=0)
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (new_last_login, user_id))
    conn.commit()
    conn.close()

def set_payment_status(status, user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    if status == 0:
        cursor.execute("UPDATE users SET is_paid = ? WHERE id = ?", (status, user_id))
        conn.commit()
        conn.close()
    elif status == 1:
        new_paytime = datetime.datetime.now().replace(microsecond=0)
        cursor.execute("UPDATE users SET pay_time = ? WHERE id = ?", (new_paytime, user_id))
        conn.commit()
        cursor.execute("UPDATE users SET is_paid = ? WHERE id = ?", (status, user_id))
        conn.commit()
        conn.close()

def add_user(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    is_paid = True
    is_admin = False
    last_login = datetime.datetime.now().replace(microsecond=0)
    last_page = 0
    now = datetime.datetime.now()
    target_datetime = now - datetime.timedelta(seconds=1)
    last_session = target_datetime.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO users (id, is_paid, is_admin, pay_time, last_login, last_page)
    VALUES (?, ?, ?, ?, ?, ?)''', (user_id, is_paid, is_admin, last_session, last_login, last_page))
    conn.commit()
    conn.close()

def check_user(user_id):
    if not select_by_id('users', user_id):
        add_user(user_id)
    else:
        user_logged(user_id)
    user_data = select_by_id('users', user_id)
    date_format = "%Y-%m-%d %H:%M:%S"
    date1 = datetime.datetime.strptime(user_data[3], date_format)
    date2 = datetime.datetime.strptime(user_data[4], date_format)
    delta = (date2 - date1).total_seconds()
    if user_data[2] == 0 and user_data[1] == 1:
        if delta > PAYMENT_PERIOD:
            set_payment_status(0, user_id)
            return False
        else:
            return True
    elif user_data[2] == 1:
        return True
    else: return False



# clear_table('users')

# drop_table('sellers')
# check_user(555581567)

# conn = sqlite3.connect('bot.db')
# cursor = conn.cursor()
# cursor.execute("UPDATE users SET is_admin = 1 WHERE id = 555581567")
# conn.commit()
# conn.close()

#
# update_page(-1, 555581567)
# print(select_all('users'))
# drop_table('users')

# #
# import sqlite3
#
# conn = sqlite3.connect('bot.db')
# cursor = conn.cursor()

# Данные для вставки
# user_id = 555581567
# is_paid = True
# is_admin = True
# last_session = '2023-01-01 10:00:00'
# last_login = '2023-01-01 11:00:00'
# last_page = 0
#
# # Вставляем данные
# cursor.execute('''
# INSERT INTO users (id, is_paid, is_admin, pay_time, last_login, last_page)
# VALUES (?, ?, ?, ?, ?, ?)''', (user_id, is_paid, is_admin, last_session, last_login, last_page))
#
# # Сохраняем изменения
# conn.commit()
#
# # Закрываем соединение
# conn.close()

