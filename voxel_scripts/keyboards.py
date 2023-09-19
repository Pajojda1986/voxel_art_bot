from aiogram.types import ReplyKeyboardMarkup
from voxel_scripts import database as db
import sqlite3 as sq

async def new_order_chat(id, type=None):
    order_artist_panel = ReplyKeyboardMarkup(resize_keyboard=True)
    order = {}
    db = sq.connect('voxel.db')
    cur = db.cursor()
    all_return = []
    cur.execute('SELECT NAME FROM sqlite_master WHERE TYPE="table"')
    print()
    all_current_tables = cur.fetchall()[1:6]
    i=0
    for table in all_current_tables:
        result = cur.execute(f"SELECT * FROM {table[0]}")
        for row in result:
            if row[type] == id: #4 для художников, 3 для заказчиков
                if row[-1]:
                    if row[-1] in order:
                        order[row[-1]].append(row[2])
                    else:
                        order[row[-1]] = []
                        order[row[-1]].extend([str(row[1]), row[2]])

    all_return.append(i)
    counts = 0
    kb_1 = []
    for item in order:
        counts += 1
        key = (f'№{" ".join(order[item])}')
        kb_1.append(key)
        i += 1
        if counts == 2:
            kb_2 = kb_1.copy()
            order_artist_panel.add(*kb_2)
            counts = 0
            kb_1.clear()
    if len(order) % 2 != 0:
        order_artist_panel.add(key)
    order_artist_panel.add('Назад')
    print(order_artist_panel)
    db.commit()
    return [i, order_artist_panel]

hands_panel = ReplyKeyboardMarkup(resize_keyboard=True)
hands_panel.add("Тонкие", "Обычные").add("Назад")

def artist_panel():
    artist_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    a = []
    counts = 0

    artists = db.get_artists_info(all=1)
    print(artists['skin'])
    artists_skins = artists['skin']
    for i in artists_skins:
        counts += 1
        a.append(i[1])
        if counts == 2:
            b = a.copy()
            artist_panel.add(*b)
            counts = 0
            a.clear()
    if len(artists_skins) % 2 != 0:
        artist_panel.add(i[1])
    print(artist_panel)
    artist_panel.add("Случайно", "Назад")

    return artist_panel


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add("Услуги", "Мои заказы").add("Отзывы")

main_multi = ReplyKeyboardMarkup(resize_keyboard=True)
main_multi.add("Услуги", "Отзывы").add("Мои заказы", "Панель администрации").add('Панель художника')

main_admins = ReplyKeyboardMarkup(resize_keyboard=True)
main_admins.add("Услуги", "Отзывы").add("Мои заказы", "Панель администрации")

artist_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
artist_keyboard.add("Товары", "Отзывы").add("Мои заказы", "Панель художника")

admins_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admins_panel.add("Таблица", "Балансы").add("Назад")

artist_personal_panel = ReplyKeyboardMarkup(resize_keyboard=True)
artist_personal_panel.add('Заказы', 'Баланс').add('Назад')

goods = ReplyKeyboardMarkup(resize_keyboard=True)
goods.add('Скин', '4D скин (Java) ').add('Плащ ', '3D аватар ').add('Тотем (2D/3D) ', 'Спец-заказ').add('Назад')

cancel_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_panel.add("Назад")

other_final_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
other_final_panel.add("Оплата").add("Назад", "Отмена заказа")

final_panel_skin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
final_panel_skin.add("Хочу!", "Нет, спасибо!").add("Назад", "Отмена заказа")

agreement_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
agreement_panel.add("Да", "Нет").add("Назад")

agreement_chat_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
agreement_chat_panel.add("Да", "Назад")

type_totem_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
type_totem_panel.add("2D", "3D").add("Назад")

photo_panel = ReplyKeyboardMarkup(resize_keyboard=True)
photo_panel.add("Назад", "Продолжить").add("Очистить")

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add('Меню')

exit_panel = ReplyKeyboardMarkup(resize_keyboard=True)
exit_panel.add("Выйти")

payment_ok = ReplyKeyboardMarkup(resize_keyboard=True)
payment_ok.add("Проверить оплату", "Назад")

exit_ord_panel = ReplyKeyboardMarkup(resize_keyboard=True)
exit_ord_panel.add("Выйти").add("Завершить заказ")