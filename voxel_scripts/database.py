import sqlite3 as sq
from datetime import datetime

db = sq.connect('voxel.db')
cur = db.cursor()


async def db_start():
    cur.execute(''' CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        id_tg INTEGER
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS skins (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        hand_type TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT,
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS totems (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        type_totem TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT,
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS cloaks (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT, 
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS skins4d (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT, 
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS avatars (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT,
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS finish_skins (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        hand_type TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT,
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS finish_totems (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        type_totem TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT,
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS finish_cloaks (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT, 
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS finish_skins4d (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT, 
        random_key TEXT
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS finish_avatars (
        id INTEGER PRIMARY KEY,
        num INTEGER,
        type TEXT,
        id_tg INTEGER,
        artist_id INTEGER,
        artist TEXT,
        amount INTEGER,
        description TEXT,
        photo TEXT,
        random_key TEXT
        )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY, 
        name TEXT,
        artist_id INTEGER,
        skin INTEGER,
        skin4d INTEGER,
        avatar INTEGER,
        cloak INTEGER,
        totem INTEGER,
        balance INTEGER
        )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        name TEXT,
        admin_id INTEGER 
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS times (
        id INTEGER PRIMARY KEY,
        time_t TEXT
        )''')
    db.commit()


def get_admins_info(all=None):
    if all == 1:
        all_admins = {
            'id': [],
            'name': []
        }
        cur.execute('SELECT * FROM admins')
        admins_table = cur.fetchall()
        for admin in admins_table:
            all_admins['id'].append(str(admin[2]))
            all_admins['name'].append(admin[1])

        print(all_admins['name'])
        return all_admins


async def get_money(id):
    db = sq.connect('voxel.db')
    cur = db.cursor()
    cur.execute(f'SELECT balance FROM artists WHERE artist_id={id}')
    all_money = cur.fetchone()[0]
    return all_money


def get_artists_info(all=None):
    if all == 1:
        all_artists = {
            'skin': [],
            'skin4d': [],
            'avatar': [],
            'cloak': [],
            'totem': []
        }

        cur.execute('SELECT * FROM artists')
        artist_table = cur.fetchall()
        for artist in artist_table:
            if artist[3] == 1:
                all_artists['skin'].append([artist[2], artist[1]])

            if artist[4] == 1:
                all_artists['skin4d'].append([artist[2], artist[1]])

            if artist[5] == 1:
                all_artists['avatar'].append([artist[2], artist[1]])

            if artist[6] == 1:
                all_artists['cloak'].append([artist[2], artist[1]])

            if artist[7] == 1:
                all_artists['totem'].append([artist[2], artist[1]])

        return all_artists

    elif all is None:
        cur.execute('SELECT artist_id FROM artists')
        artist_id = cur.fetchall()
        id = []
        for i in artist_id:
            id.append(str(*i))
        return id


    elif all == 2:
        cur.execute('SELECT name FROM artists')
        artists_name = cur.fetchall()
        print(artists_name)
        return artists_name

    elif all == 3:
        cur.execute('SELECT name, artist_id FROM artists')
        all_artists = cur.fetchall()
        return all_artists


async def get_balance():
    name_id = get_artists_info(all=3)
    db = sq.connect('voxel.db')
    cur = db.cursor()
    message = ''

    for id in name_id:
        print(id)
        cur.execute(f'SELECT balance, name FROM artists WHERE artist_id={id[1]}')
        all_data = cur.fetchone()
        message += (f'Баланс {all_data[1]}: {all_data[0]} рублей\n')

    return message

async def new_count_order():
    data = f"{datetime.now(): {'%Y-%m-%d %H:%M'}}"
    current_date = str(data)[1:].replace(' ', '-')
    time_order = f"""INSERT INTO times (time_t) VALUES(?);"""
    cur.execute(time_order, (current_date,))
    db.commit()

async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE id_tg == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (id_tg) VALUES ({key})".format(key=user_id))
        db.commit()

async def skin_4d(ord, message, var=1):
    if var == 1:
        result = cur.execute("SELECT * FROM times ORDER BY id DESC LIMIT 1")
        num = result.fetchone()[0]
        await message.bot.send_message(ord[1], f'Вам пришёл новый заказ! Его номер {num}')
        final_order = f"""INSERT INTO skins4d (num, type, id_tg, artist_id, artist, amount, description, photo, random_key) VALUES(
        {num},
        '4D_Скин', 
        {ord[0]},
        {ord[1]},
        '{ord[2]}',
        {ord[3]},
        '{ord[4]}',
        "{ord[5]}",
        '{ord[6]}')"""
        cur.execute(final_order)
        db.commit()
    if var == 2:
        final_order = f"""INSERT INTO finish_skins4d (num, type, id_tg, artist_id, artist, amount, description, photo, random_key) VALUES(
        {ord[1]},
        '{ord[2]}',
        {ord[3]},
        {ord[4]},
        '{ord[5]}',
        {ord[6]},
        '{ord[7]}',
        "{ord[8]}",
        '{ord[9]}')"""
        cur.execute(final_order)
        db.commit()

    if var == 3:
        cur.execute(f"""SELECT amount, artist_id FROM skins4d WHERE num={ord}""")
        meta = cur.fetchone()
        cur.execute(f'''SELECT balance FROM artists WHERE artist_id={meta[1]}''')
        new_balance = cur.fetchone()[0] + (meta[0] // 2)
        cur.execute(f"""UPDATE artists SET balance = {new_balance} WHERE artist_id={meta[1]}""")
        final_order = f"""DELETE FROM skins4d WHERE num={ord}"""
        cur.execute(final_order)
        db.commit()

async def totem(ord, message, var=1):
    if var == 1:
        result = cur.execute("SELECT * FROM times ORDER BY id DESC LIMIT 1")
        num = result.fetchone()[0]
        await message.bot.send_message(ord[1], f'Вам пришёл новый заказ! Его номер {num}')
        final_order = f"""INSERT INTO totems (num, id_tg, type, artist_id, artist, type_totem, amount, description, photo, random_key) VALUES(
        {num},
        {ord[0]},
        'тотем',
        {ord[1]},
        '{ord[2]}',
        '{ord[3]}',
        {ord[4]},
        '{ord[5]}',
        "{ord[6]}",
        '{ord[7]}')"""
        cur.execute(final_order)
        db.commit()

    if var == 2:
        final_order = f"""INSERT INTO finish_totems (num, type, id_tg, artist_id, artist, type_totem, amount, description, photo, random_key) VALUES(
        {ord[1]},
        '{ord[2]}',
        {ord[3]},
        {ord[4]},
        '{ord[5]}',
        '{ord[6]}',
        {ord[7]},
        '{ord[8]}',
        "{ord[9]}",
        '{ord[10]}')"""
        cur.execute(final_order)
        db.commit()

    if var == 3:
        cur.execute(f"""SELECT amount, artist_id FROM totems WHERE num={ord}""")
        meta = cur.fetchone()
        cur.execute(f'''SELECT balance FROM artists WHERE artist_id={meta[1]}''')
        new_balance = cur.fetchone()[0] + (meta[0] // 2)
        cur.execute(f"""UPDATE artists SET balance = {new_balance} WHERE artist_id={meta[1]}""")
        final_order = f"""DELETE FROM totems WHERE num={ord}"""
        cur.execute(final_order)
        db.commit()

async def skin(ord, message, var=1):
    if var == 1:
        result = cur.execute("SELECT * FROM times ORDER BY id DESC LIMIT 1")
        num = result.fetchone()[0]
        await message.bot.send_message(ord[1], f'Вам пришёл новый заказ! Его номер {num}')
        final_order = f"""INSERT INTO skins (num, id_tg, type, artist_id, artist, hand_type, amount, description, photo, random_key) VALUES(
        {num},
        {ord[0]},
        'скин',
        {ord[1]},
        '{ord[2]}',
        '{ord[3]}',
        {ord[4]},
        '{ord[5]}',
        "{ord[6]}",
        '{ord[7]}')"""
        cur.execute(final_order)
        db.commit()

    if var == 2:
        final_order = f"""INSERT INTO finish_skins (num, type, id_tg, artist_id, artist, hand_type, amount, description, photo, random_key) VALUES(
        {ord[1]},
        '{ord[2]}',
        {ord[3]},
        {ord[4]},
        '{ord[5]}',
        '{ord[6]}',
        {ord[7]},
        '{ord[8]}',
        "{ord[9]}",
        '{ord[10]}')"""
        cur.execute(final_order)
        db.commit()
    if var == 3:
        cur.execute(f"""SELECT amount, artist_id FROM skins WHERE num={ord}""")
        meta = cur.fetchone()
        cur.execute(f'''SELECT balance FROM artists WHERE artist_id={meta[1]}''')
        new_balance = cur.fetchone()[0] + (meta[0] // 2)
        cur.execute(f"""UPDATE artists SET balance = {new_balance} WHERE artist_id={meta[1]}""")
        final_order = f"""DELETE FROM skins where num={ord}"""
        cur.execute(final_order)
        db.commit()


async def cloak(ord, message, var=1):
    if var == 1:
        result = cur.execute("SELECT * FROM times ORDER BY id DESC LIMIT 1")
        num = result.fetchone()[0]
        await message.bot.send_message(ord[1], f'Вам пришёл новый заказ! Его номер {num}')
        final_order = f"""INSERT INTO cloaks (num, id_tg, type, artist_id, artist, amount, description, photo, random_key) VALUES(
        {num},
        {ord[0]}, 
        'плащ', 
        {ord[1]}, 
        '{ord[2]}',
        {ord[3]}, 
        '{ord[4]}', 
        "{ord[5]}",
        '{ord[6]}')"""

        cur.execute(final_order)
        db.commit()
    if var == 2:
        final_order = f"""INSERT INTO finish_cloaks (num, type, id_tg, artist_id, artist, amount, description, photo, random_key) VALUES(
        {ord[1]},
        '{ord[2]}',
        {ord[3]},
        {ord[4]},
        '{ord[5]}',
        {ord[6]},
        '{ord[7]}',
        "{ord[8]}",
        '{ord[9]}') """
        cur.execute(final_order)
        db.commit()
    if var == 3:
        cur.execute(f"""SELECT amount, artist_id FROM cloaks WHERE num={ord}""")
        meta = cur.fetchone()
        cur.execute(f'''SELECT balance FROM artists WHERE artist_id={meta[1]}''')
        new_balance = cur.fetchone()[0] + (meta[0] // 2)
        cur.execute(f"""UPDATE artists SET balance = {new_balance} WHERE artist_id={meta[1]}""")
        final_order = f"""DELETE FROM cloaks where num={ord}"""
        cur.execute(final_order)
        db.commit()

async def avatar(ord, message, var=1):
    if var == 1:
        result = cur.execute("SELECT * FROM times ORDER BY id DESC LIMIT 1")
        num = result.fetchone()[0]
        await message.bot.send_message(ord[1], f'Вам пришёл новый заказ! Его номер {num}')
        final_order = f"""INSERT INTO avatars (num, id_tg, type, artist_id, artist, amount, description, photo, random_key) VALUES(
        {num},
        {ord[0]},
        'аватар', 
        {ord[1]}, 
        '{ord[2]}', 
        {ord[3]},
        '{ord[4]}', 
        "{ord[5]}",
        '{ord[6]}')"""
        cur.execute(final_order)
        db.commit()

    if var == 2:
        final_order = f"""INSERT INTO finish_avatars (num, type, id_tg, artist_id, artist, amount, description, photo, random_key) VALUES(
        {ord[1]},
        '{ord[2]}',
        {ord[3]},
        {ord[4]},
        '{ord[5]}',
        {ord[6]},
        '{ord[7]}',
        "{ord[8]}",
        '{ord[9]}')"""
        cur.execute(final_order)
        db.commit()

    if var == 3:
        cur.execute(f"""SELECT amount, artist_id FROM avatars WHERE num={ord}""")
        meta = cur.fetchone()
        cur.execute(f'''SELECT balance FROM artists WHERE artist_id={meta[1]}''')
        new_balance = cur.fetchone()[0] + (meta[0] // 2)
        cur.execute(f"""UPDATE artists SET balance = {new_balance} WHERE artist_id={meta[1]}""")
        final_order = f"""DELETE FROM avatars where num={ord}"""
        cur.execute(final_order)
        db.commit()
