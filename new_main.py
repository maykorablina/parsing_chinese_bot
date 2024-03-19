import asyncio
import random
import database as db
import functions as fx
from functions import sort_format, get_inline_keyboard
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from functions import PAYMENT_PERIOD, TOKEN_API
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN_API = TOKEN_API
bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def get_info(message):
    user_id = message.from_user.id
    # print(user_id)
    # if not fx.is_directory_empty('data'):
    kb = [[types.KeyboardButton(text="/start")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    if db.check_user(user_id):
        shop = db.select_and_delete()
        if shop:
            shop = shop[1].split(';')
            msg = f"<b>Магазин: {shop[1]}</b>\n<b>Регион: {shop[2]}</b>\n<b>Был в сети: {shop[3]}</b>\n<b>Кол-во отзывов: {shop[0]}</b>\n<b>Ссылка: {shop[4].strip()}</b>"
            await message.answer(msg, reply_markup = keyboard)
    else:
        shop = db.select_and_delete()
        if shop:
            shop = shop[1].split(';')
            msg = f"<b>Магазин: {shop[1]}</b>\n<b>Регион: {shop[2]}</b>\n<b>Был в сети: {shop[3]}</b>\n<b>Кол-во отзывов: {shop[0]}</b>\n<b>Ссылка: {shop[4].strip()}</b>"
            await message.answer(msg, reply_markup=keyboard)






    # # if not fx.is_directory_empty('data'):
    # #     print("появились новые файлы")
    # #     data = fx.sort_format('data')
    # #     print('файлы прочитаны')
    # #     db.reset_data(data)
    # #     print("база данных обновилась")
    # #     fx.delete_files('data')
    # #     print('файлы удалились')
    # msg = db.select_and_delete()
    # # УБРАТЬ ПРИ ПЕРВОЙ ВОЗМОЖНОСТИ!!!
    # if msg:
    #     message = await message.answer(msg[1], reply_markup=keyboard)
    # else:
    #     message = await message.answer("<b>Селлеры с недавним онлайном закончились</b>")



    # print(db.select_all('sellers'))
    # print(db.select_and_delete())

    # if not db.check_user(user_id):
    #     msg = await message.answer(text='<b>Бот не оплачен</b>')
    # else:
    # print(sort_format('data'))



        # print(db.select_by_id('users', user_id))

#         data = sort_format('data')
#         db.reset_data(data)
#         db.update_page(0, message.from_user.id, default=True)
#         kb = [
#             [types.KeyboardButton(text="/start"), types.KeyboardButton(text="/payment")]
#         ]
#         keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
#         msg = await message.answer(text = 'ㅤ', reply_markup = keyboard)
#         # await msg.delete()
#         await message.answer(db.select_by_id('sellers', 0)[1], reply_markup = get_inline_keyboard(0, db.n_sellers()))
#
#
# @dp.callback_query(F.data.startswith('fwd'))
# async def go_fwd(callback: types.CallbackQuery):
#     cur_page = db.update_page(1, callback.from_user.id)
#     await callback.message.edit_text(
#         text=db.select_by_id('sellers', cur_page)[1],
#         reply_markup=get_inline_keyboard(cur_page, db.n_sellers())
#     )
#
# @dp.callback_query(F.data.startswith('back'))
# async def go_back(callback: types.CallbackQuery):
#     cur_page = db.update_page(-1, callback.from_user.id)
#     await callback.message.edit_text(
#         text=db.select_by_id('sellers', cur_page)[1],
#         reply_markup=get_inline_keyboard(cur_page, db.n_sellers())
#     )
#
# @dp.message(Command("payment"))
# async def payment(message):
#     user_data = db.select_by_id('users', message.from_user.id)
#     if user_data[1] == 0 and user_data[2] == 0:
#         if user_data[3] == '2008-01-01 10:00:00':
#             await message.answer(f"<b>Бот не оплачен</b>\n\n<b>Бот еще ни разу не оплачивали</b>{user_data[3]}",
#                                  reply_markup=fx.payment_inline_keyboard())
#
#         else: await message.answer(f"<b>Бот не оплачен</b>\n\n<b>Дата последней оплаты: </b>{user_data[3]}",reply_markup = fx.payment_inline_keyboard())
#     elif user_data[2] == 1:
#         await message.answer(f"<b>Ты админ, тебе нихуя не надо в этой жизни</b>\n\n<b>Можешь мне деньги по рофлу скинуть</b>",reply_markup = fx.payment_inline_keyboard())
#     else:
#         d = fx.time_delta(user_data[4], user_data[3])
#         text = f"{d[0]} дней, {d[1]} часов, {d[2]} минут"
#         await message.answer(f"<b>Бот оплачен</b>\n\n<b>Подписка истекает через: </b>{text}",reply_markup = fx.payment_inline_keyboard())



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
#1246856201