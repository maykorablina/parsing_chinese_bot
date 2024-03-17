import datetime
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

PAYMENT_PERIOD = 86400
MERCHANT_ID = '1436c32e-4562-48ce-a7c4-da5f088df58c'
TOKEN_API = '7001822994:AAH6Jg8yoIkITTs0HwsTVk_kJOdteTXt4fo'

def delete_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении {file_path}. Причина: {e}')

def parse_files(directory):
    content = ''
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            with open(os.path.join(directory, filename), 'r') as file:
                content += file.read() + '\n'
    return content


def sort_format(directory):
    data_list = [x.split(';') for x in parse_files(directory).split('\n') if x.split(';') != ['']]
    suitable = ['1 day ago']
    res = []
    shop_titles = set()
    for shop in data_list:
        if shop[2] in suitable and shop[1] not in shop_titles and int(shop[0]) < 5:
            msg = f"<b>Магазин: {shop[1]}</b>\n<b>Был в сети: {shop[2]}</b>\n<b>Кол-во отзывов: {shop[0]}</b>\n<b>Ссылка: {shop[3].strip()}</b>"
            shop_titles.add(shop[1])
            res.append(msg)
    return res


def is_directory_empty(path):
    a = list(os.listdir(path))
    if not a:
        return True
    else:
        return False


def get_inline_keyboard(page, pages):
    builder = InlineKeyboardBuilder()
    if page == 0:
        builder.row(
            InlineKeyboardButton(
                text=f'{page + 1}/{pages}', callback_data='sth'
            ))
        builder.row(
            InlineKeyboardButton(
                text=">>>", callback_data=f'fwd_{page}_{pages}'
            )
        )

    elif page + 1 == pages:
        builder.row(
            InlineKeyboardButton(
                text=f'{page + 1}/{pages}', callback_data='sth'
            ))
        builder.row(
            InlineKeyboardButton(
                text="<<<", callback_data=f'back_{page}_{pages}',
            ))

    else:
        builder.row(InlineKeyboardButton(
            text=f'{page + 1}/{pages}', callback_data='sth'
        ))
        builder.row(
            InlineKeyboardButton(
                text="<<<", callback_data=f'back_{page}_{pages}',
            ),
            InlineKeyboardButton(
                text=">>>", callback_data=f'fwd_{page}_{pages}'
            ), width=3
        )

    return builder.as_markup()


def payment_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'Оплатить', callback_data='pay'
        ))
    builder.row(
        InlineKeyboardButton(
            text=f'Проверить оплату', callback_data='check'
        ))

    return builder.as_markup()


def time_delta(time1, time2):
    date_format = "%Y-%m-%d %H:%M:%S"
    date1 = datetime.datetime.strptime(time1, date_format)
    date2 = datetime.datetime.strptime(time2, date_format)
    delta = (date2 - date1)
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes, seconds

# def time_to_pay(PAYMENT_PERIOD):
#     now = datetime.datetime.now()
#     target_datetime = now - datetime.timedelta(seconds=PAYMENT_PERIOD)
#     days = target_datetime.days
#     hours, remainder = divmod(target_datetime.seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     return (days, hours, minutes, seconds)
