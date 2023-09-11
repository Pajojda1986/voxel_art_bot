from aiogram import types
from aiogram.types.message import ContentType
from random import randint, choices
import string
import os
import sqlite3 as sq
from voxel_scripts import database as db
from aiogram.dispatcher import FSMContext
from voxel_scripts import keyboards as kb
from voxel_scripts import class_voxel as cls
from voxel_scripts.payments import order, order_2, order_3

from main import dp, bot

all_photo = {}
all_cloak = {}
all_totem = {}
all_4d = {}
all_3D_avatar = {}

async def get_ord_skin(message, state, dictionary, rand=None, price=None):

    data = await state.get_data()
    hand_type = data.get('hand_type')
    artist_name = data.get('artist')
    artist_id = data.get('artist_id')

    description = data.get('description')

    ord = (message.from_user.id, artist_id, artist_name, hand_type, price, description, dictionary[message.from_user.id], rand)
    print(ord)
    return ord


async def get_ord_other(message, state, dictionary, type_ord, artist_id=None, artist_name=None, totem_type=None, rand=None, price=None):
    data = await state.get_data()

    if artist_id is None and artist_name is None:
        artist = db.get_artists_info(all=1)
        artist_name = []
        artist_id = []
        for i in artist['skin']:
            artist_name.append(i[1])
            artist_id.append(i[0])

        random_id = randint(0, len(artist_name) - 1)
        artist_name = artist_name[random_id]
        artist_id = artist_id[random_id]

    description = data.get(type_ord)
    if totem_type is not None:
        ord = (message.from_user.id, artist_id, artist_name, totem_type, price, description, dictionary[message.from_user.id], rand)
        return ord
    else:
        ord = (message.from_user.id, artist_id, artist_name, price, description, dictionary[message.from_user.id], rand)
        return ord


async def final_other(message, state, count_photo, dictionary, name_order, type=None):
    data = await state.get_data()
    description = data.get('description')

    await message.answer("Ваш финальный заказ:")
    if type is not None:
        await message.answer(f"Описание вашего {name_order}: {description},\nТип {name_order}: {type}",
                             reply_markup=kb.other_final_panel)
    else:
        await message.answer(f"Описание вашего {name_order}: {description}", reply_markup=kb.other_final_panel)
    if len(dictionary[message.from_user.id]) == 0:
        await message.answer("Вы не приложили файлы или фотографии")

    else:
        if len(dictionary[message.from_user.id]) > count_photo:
            await message.answer(f"Все фотографии или файлы больше {count_photo} были удалены!")
            del dictionary[message.from_user.id][count_photo:]
        for i in dictionary[message.from_user.id]:
            try:
                await bot.send_photo(message.chat.id, str(i))
            except:
                pass
            try:
                await bot.send_document(message.chat.id, str(i))
            except:
                pass


async def final_order(message, state, key=1):
    data = await state.get_data()
    hand_type = data.get('hand_type')
    artist = data.get('artist')
    description = data.get('description')
    totem_type = data.get('totem_type')
    description_cloak = data.get('cloak_description')
    description_totem = data.get("totem_description")
    await message.answer("Ваш финальный заказ:")

    await message.answer(f"Выбраный вами тип рук: {hand_type},\nВыбраный вами художник: {artist},"
                         f"\nВаше описание: {description}", reply_markup=kb.final_panel_skin)

    if len(all_photo[message.from_user.id]) == 0:
        await message.answer("Вы не приложили файлы или фотографии")

    else:
        if len(all_photo[message.from_user.id]) > 5:
            await message.answer("Все фотографии или файлы больше пяти были удалены!")
            del all_photo[message.from_user.id][5:]
        for i in all_photo[message.from_user.id]:
            try:
                await bot.send_photo(message.chat.id, str(i))
            except:
                pass
            try:
                await bot.send_document(message.chat.id, str(i))
            except:
                pass

    if description_totem and description_totem != "Назад" and description_totem != "Продолжить" and key == 1:
        print(description_totem)
        await message.answer(f"Описание тотема: {description_totem},"
                             f"\nТип тотема: {totem_type}", reply_markup=kb.other_final_panel)

        if len(all_totem[message.from_user.id]) == 0:
            await message.answer("Вы не приложили файлы или фотографии")

        else:
            if len(all_totem[message.from_user.id]) > 2:
                await message.answer("Все фотографии или файлы больше двух были удалены!")
                del all_totem[message.from_user.id][2:]
            for i in all_totem[message.from_user.id]:
                try:
                    await bot.send_photo(message.chat.id, str(i))
                except:
                    pass
                try:
                    await bot.send_document(message.chat.id, str(i))
                except:
                    pass

    if description_cloak and description_cloak != "Назад" and description_cloak != "Продолжить" and key == 1:
        await message.answer(f"Описание плаща: {description_cloak}", reply_markup=kb.other_final_panel)

        if len(all_cloak[message.from_user.id]) == 0:
            await message.answer("Вы не приложили файлы или фотографии")

        else:
            if len(all_cloak[message.from_user.id]) > 3:
                await message.answer("Все фотографии или файлы больше двух были удалены!")
                del all_cloak[message.from_user.id][2:]
            for i in all_cloak[message.from_user.id]:
                try:
                    await bot.send_photo(message.chat.id, str(i))
                except:
                    pass
                try:
                    await bot.send_document(message.chat.id, str(i))
                except:
                    pass

async def order_photo(message, dictionary):
    try:
        if message.document:
            documents_id = message.document.file_id
            dictionary[message.from_user.id].append(documents_id)
            print(dictionary[message.from_user.id])
            print('документ')

    except:
        if message.photo:
            photo_id = message.photo[2].file_id
            dictionary[message.from_user.id].append(photo_id)
            print(dictionary[message.from_user.id])
            print('фото')

    if message.text == 'Очистить':
        del dictionary[message.from_user.id][::]
        await message.answer("Список фотографий или файлов был очищен!", reply_markup=kb.photo_panel)


@dp.message_handler(text='Меню')
@dp.message_handler(commands=['start'])
@dp.message_handler(text='Назад')
async def cmd_start(message: types.Message):
    db.get_artists_info()
    all_photo[message.from_user.id] = []
    all_totem[message.from_user.id] = []
    all_cloak[message.from_user.id] = []
    await db.cmd_start_db(message.from_user.id)
    await message.answer(f'🤖 Добро пожаловать {message.from_user.first_name}! Я - Воксель, бот, '
                         f'который поможет Вам с заказом. Чтобы оформить заказ, '
                         f'напишите "Товары" или нажмите соответствующую кнопку. 👇', reply_markup=kb.main)

    print(message.chat.id)
    if str(message.from_user.id) in db.get_artists_info():
        await message.answer(f'Вы авторизовались как художник', reply_markup=kb.artist_keyboard)


@dp.message_handler(text='Отзывы', state=None)
async def cmd_text(message: types.Message):
    await message.answer('Посмотреть отзывы Вы сможете в нашей группе VK https://vk.com/lootskinsstudio?w=app6326142_-222235507')

@dp.message_handler(text='Услуги', state=None)
async def cmd_text(message: types.Message):
    await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)

@dp.message_handler(text='Спец-заказ', state=None)
async def spez(message: types.Message):
    await message.answer('Если вы хотите заказать сразу несколько скинов или прочих товаров, а также текстурпак,'
                         ' 3D арт или что то другое, напишите нам в сообщения сообщества ВК, для обсуждения условий. '
                         'Ссылка на группу: https://vk.com/lootskinsstudio')

@dp.message_handler(text='Тотем (2D/3D)', state=None)
async def totem(message: types.Message):
    all_totem[message.from_user.id] = []
    await message.answer('Какой предмет игрок чаще всего носит в руке? '
                         'Конечно, тотем бессмертия! Из него можно сделать абсолютно всё - от забавной статуэтки с '
                         'Вашим персонажем до магического кристалла.', reply_markup=kb.cancel_panel)
    await message.answer('Сначала выберите, каким будет Ваш тотем - 2D или 3D', reply_markup=kb.type_totem_panel)

    await cls.OrderTotem.type.set()


@dp.message_handler(state=cls.OrderTotem.type, content_types=["text"])
async def totem(message: types.Message, state: FSMContext):
    if message.text == '2D' or message.text == '3D':
        item = message.text
        await state.update_data(
            {
                'totem_type': item
            }
        )
        await message.answer("Напишите, что Вы хотите видеть в качестве тотема.", reply_markup=kb.cancel_panel)
        await cls.OrderTotem.next()

    elif message.text == 'Назад' or message.text == 'Отмена':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()

    else:
        await message.answer("Выберете тип тотема! Если вы хотите отменить составление заказа введите 'Отмена'")


@dp.message_handler(state=cls.OrderTotem.description, content_types=["text"])
async def totem(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" or message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        print(item)
        await state.update_data(
            {
                'description': item
            }
        )

    if message.text != 'Назад' and not "'" in message.text and not '"' in message.text:
        await message.answer("Теперь приложите до 2 фотографий-референсов в формате "
                             ".jpeg или развёртку вашего скина в формате .png без сжатия, "
                             "фотографии лучше присылать отдельными сообщениями! "
                             "После чего нажмите кнопку 'Продолжить'", reply_markup=kb.photo_panel)
        await cls.OrderTotem.next()

    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == "Назад":
        await message.answer("Выберите, каким будет Ваш тотем - 2D или 3D", reply_markup=kb.type_totem_panel)
        await cls.OrderTotem.previous()


@dp.message_handler(state=cls.OrderTotem.photo, content_types=['document', 'photo', 'text'])
async def avatar(message: types.Message, state: FSMContext):
    await order_photo(message, all_totem)
    data = await state.get_data()
    type_totem = data.get('totem_type')

    if message.text == 'Продолжить':
        await final_other(message, state, 2, all_totem, 'Тотема', type=type_totem)

    elif message.text == "Оплата":
        if type_totem == "2D":
            await order(message, bot, ord='2D тотем', price_1=49)

        elif type_totem == "3D":
            await order(message, bot, ord='3D тотем', price_1=79)

    elif message.text == 'Назад':
        await message.answer('Опишите, как должен выглядеть будущий Тотем, '
                             'если вы хотите оставить описание прежним, '
                             'введите продолжить', reply_markup=kb.cancel_panel)
        await cls.OrderTotem.description.set()

    elif message.text == 'Отмена заказа':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderTotem.photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderTotem.photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')

    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))

    data = await state.get_data()
    type_totem = data.get('totem_type')
    if type_totem == "2D":
        ord = await get_ord_other(message, state, all_totem, 'description', totem_type=type_totem, rand=ran, price=49)
    else:
        ord = await get_ord_other(message, state, all_totem, 'description', totem_type=type_totem, rand=ran, price=79)

    await db.new_count_order()
    await db.totem(ord, message=message)
    await message.answer('Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer('Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(text='3D аватар', state=None)
async def avatar(message: types.Message):
    all_3D_avatar[message.from_user.id] = []
    await message.answer('👨 Уникальное фото профиля с Вашим персонажем!', reply_markup=kb.cancel_panel)
    await message.answer('Опишите, как должен выглядеть будущий аватар')

    await cls.Order3dAvatar.description.set()


@dp.message_handler(state=cls.Order3dAvatar.description, content_types=["text"])
async def avatar(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" or message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        print(item)
        await state.update_data(
            {
                'description': item
            }
        )


    if message.text != 'Назад' and "'" not in message.text and not'"' in message.text:
        await message.answer("Теперь приложите до 3 фотографий-референсов в формате "
                             ".jpeg, а также обязательно развёртку вашего скина в формате .png без сжатия, "
                             "фотографии лучше присылать отдельными сообщениями!", reply_markup=kb.photo_panel)
        await cls.Order3dAvatar.next()

    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == "Назад":
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.message_handler(state=cls.Order3dAvatar.photo, content_types=['document', 'photo', 'text'])
async def avatar(message: types.Message, state: FSMContext):
    await order_photo(message, all_3D_avatar)

    if message.text == 'Продолжить':
        await final_other(message, state, 3, all_3D_avatar, 'Аватара')

    elif message.text == "Оплата":
        await order(message, bot, ord='Плащ', price_1=199)

    elif message.text == 'Назад':
        await message.answer('Опишите, как должен выглядеть будущий 3D Аватар', reply_markup=kb.cancel_panel)
        await cls.Order3dAvatar.description.set()

    elif message.text == 'Отмена заказа':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.pre_checkout_query_handler(lambda query: True, state=cls.Order3dAvatar.photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.Order3dAvatar.photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    ord = await get_ord_other(message, state, all_3D_avatar, 'description', rand=ran, price=199)
    await db.new_count_order()
    await db.avatar(ord, message=message)
    await message.answer('Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(text='Плащ', state=None)
async def cloak(message: types.Message):
    all_cloak[message.from_user.id] = []
    await message.answer('Майнкрафт предлагает ограниченное количество плащей, '
                         'да и получить их не так просто, но с помощью мода Advanced Capes Mod можно '
                         'установить плащ с совершенно любым рисунком! '
                         'Мы сделаем его по Вашему описанию!', reply_markup=kb.cancel_panel)
    await message.answer('Опишите, как должен выглядеть будущий плащ')

    await cls.OrderCloak.description.set()


@dp.message_handler(state=cls.OrderCloak.description, content_types=["text"])
async def cloak(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" or message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        await state.update_data(
            {
                'description': item
            }
        )

    if message.text != 'Назад' and not "'" in message.text and '"' not in message.text:
        await message.answer("Теперь приложите до 4 фотографий-референсов в формате "
                             ".jpeg или развёртку вашего скина в формате .png без сжатия, "
                             "фотографии лучше присылать отдельными сообщениями!", reply_markup=kb.photo_panel)
        await cls.OrderCloak.next()

    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == "Назад":
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.message_handler(state=cls.OrderCloak.photo, content_types=['document', 'photo', 'text'])
async def cloak(message: types.Message, state: FSMContext):
    await order_photo(message, all_cloak)

    if message.text == 'Продолжить':
        await final_other(message, state, 4, all_cloak, 'Плаща')

    elif message.text == 'Оплата':
        await order(message, bot, ord='Плащ', price_1=79)

    elif message.text == 'Назад':
        await message.answer('Опишите, как должен выглядеть будущий Плащ', reply_markup=kb.cancel_panel)
        await cls.OrderCloak.description.set()

    elif message.text == 'Отмена заказа':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderCloak.photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderCloak.photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    ord = await get_ord_other(message, state, all_cloak, 'description', rand=ran, price=79)
    await db.new_count_order()
    await db.cloak(ord, message=message)
    await message.answer(
        'Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(text='4D скин (Java)', state=None)
async def skin4D(message: types.Message):
    all_4d[message.from_user.id] = []
    await message.answer('4D скин - неповторимая модель Вашего персонажа! '
                         'Для того, чтобы использовать 4D скин, необходим мод Figura: '
                         'https://modrinth.com/mod/figura подробнее о том, как установить такой скин: '
                         'ссылка на статью', reply_markup=kb.cancel_panel)
    await message.answer('Опишите, как должен выглядеть будущий 4D скин.')

    await cls.OrderSkin4D.description.set()


@dp.message_handler(state=cls.OrderSkin4D.description, content_types=["text"])
async def skin4D(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" or message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        print(item)
        await state.update_data(
            {
                'description': item
            }
        )

    if message.text != 'Назад' and "'" not in message.text and '"' not in message.text:
        await message.answer("Теперь приложите до 5 фотографий-референсов в формате "
                             ".jpeg или развёртку вашего скина в формате .png без сжатия, "
                             "фотографии лучше присылать отдельными сообщениями!", reply_markup=kb.photo_panel)
        await cls.OrderSkin4D.next()

    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == "Назад":
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.message_handler(state=cls.OrderSkin4D.photo, content_types=['document', 'photo', 'text'])
async def skin4D(message: types.Message, state: FSMContext):
    await order_photo(message, all_4d)

    if message.text == 'Продолжить':
        await final_other(message, state, 5, all_4d, '4D скина')

    elif message.text == 'Назад':
        await message.answer('Опишите, как должен выглядеть будущий 4D скин.', reply_markup=kb.cancel_panel)
        await cls.OrderSkin4D.description.set()

    elif message.text == 'Оплата':
        await order(message, bot, ord='4D Скин', price_1=399)

    elif message.text == 'Отмена заказа':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderSkin4D.photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderSkin4D.photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    ord = await get_ord_other(message, state, all_4d, 'description', rand=ran, price=399)
    await db.new_count_order()
    await db.skin_4d(ord, message=message)
    await message.answer(
        'Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(text='Скин', state=None)
async def order_skin(message: types.Message):
    all_photo[message.from_user.id] = []
    all_totem[message.from_user.id] = []
    all_cloak[message.from_user.id] = []
    await message.answer('Давайте выберем, какие руки будут у Вашего скина - '
                         'стандартные, как у Стива, или тонкие, как у Алекс?', reply_markup=kb.hands_panel)

    await cls.OrderSkin.hand_type.set()


@dp.message_handler(state=cls.OrderSkin.hand_type, content_types=["text"])
async def order_skin(message: types.Message, state: FSMContext):
    if message.text == 'Тонкие' or message.text == 'Обычные':
        item = message.text
        await state.update_data(
            {
                'hand_type': item
            }
        )
        await message.answer("👨‍🎨 У нас работает несколько талантливых художников, "
                             "у каждого из которых свой неповторимый стиль! Вы можете выбрать того, "
                             "кто будет выполнять Ваш заказ или отдать его "
                             "случайному художнику 🎲", reply_markup= kb.artist_panel())
        await cls.OrderSkin.next()

    elif message.text == 'Назад' or message.text == 'Отмена':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()

    else:
        await message.answer("Выберете тип рук! Если вы хотите отменить составление заказа введите 'Отмена'")


@dp.message_handler(state=cls.OrderSkin.artist)
async def order_skin(message: types.Message, state: FSMContext):
    artist = db.get_artists_info(all=1)
    artist_name = []
    artist_id = []
    for i in artist['skin']:
        artist_name.append(i[1])
        artist_id.append(i[0])

    if message.text in artist_name or message.text == 'Случайно':
        if message.text != 'Случайно':
            for i in artist_name:
                if message.text == i:
                    name = i
                    id = artist_id[artist_name.index(i)]
                    await state.update_data(
                        {
                            'artist': name,
                            'artist_id': id
                        }
                    )
                    await message.answer("Опишите, как должен выглядеть будущий скин. ", reply_markup=kb.cancel_panel)
                    await cls.OrderSkin.next()

        elif message.text == 'Случайно':
            random_id = randint(0, len(artist_name) - 1)
            random_artist = artist_name[random_id]
            random_artist_id = artist_id[random_id]
            print(random_artist)
            print(random_artist_id)

            await state.update_data(
                {
                    'artist': random_artist,
                    'artist_id': random_artist_id
                }
            )
            await message.answer("Опишите, как должен выглядеть будущий скин. "
                                 "Приложить файлы или фото можно будет в следующем шаге", reply_markup=kb.cancel_panel)
            await cls.OrderSkin.next()

    elif message.text == 'Назад':
        await cls.OrderSkin.previous()
        await message.answer('Давайте выберем, какие руки будут у Вашего скина - стандартные, '
                             'как у Стива, или тонкие, как у Алекс?', reply_markup=kb.hands_panel)

    elif message.text == 'Отмена':
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()

    else:
        await message.answer('Выберете художника! Если вы хотите отменить '
                             'составление заказа впишите "Отмена"', reply_markup = kb.artist_panel())


@dp.message_handler(state=cls.OrderSkin.description)
async def order_skin(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" and message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        print(item)
        await state.update_data(
            {
                'description': item
            }
        )

    if message.text != 'Назад' and "'" not in message.text and not '"' in message.text:
        await message.answer("Теперь приложите до 5 фотографий-референсов в формате "
                             ".jpeg или развёртку вашего скина в формате .png без сжатия, фотографии "
                             "лучше присылать отдельными сообщениями!", reply_markup=kb.photo_panel)
        await cls.OrderSkin.next()
    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == 'Назад':
        await cls.OrderSkin.previous()
        await message.answer("👨‍🎨 У нас работает несколько талантливых художников, "
                             "у каждого из которых свой неповторимый стиль! Вы можете выбрать того, кто будет "
                             "выполнять Ваш заказ или отдать его случайному художнику 🎲", reply_markup = kb.artist_panel())


@dp.message_handler(state=cls.OrderSkin.photo, content_types=['document', 'photo', 'text'])
async def order_skin(message: types.Message, state: FSMContext):
    await order_photo(message, all_photo)

    if message.text == 'Продолжить':

        await final_order(message, state, key=2)
        await message.answer('Хотите добавить что-нибудь ещё к Вашему заказу, например, тотем или плащ? 😁')

    elif message.text == 'Хочу!':
        await message.answer('Хотите ли вы добавить к заказу тотем?', reply_markup=kb.agreement_panel)
        await cls.OrderSkin.additional_goods.set()

    elif message.text == "Нет, спасибо!":
        await order(message, bot, ord='Скин', price_1=249)

    elif message.text == "Отмена заказа":
        await message.answer('Выберите услугу ✏️', reply_markup=kb.goods)
        await state.finish()

    elif message.text == "Назад":
        await message.answer("Опишите, как Вы представляете Ваш будущий скин! "
                             "Чтобы оставить описание прежним введите 'Продолжить'", reply_markup=kb.cancel_panel)
        await cls.OrderSkin.previous()


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderSkin.photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderSkin.photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    ord = await get_ord_skin(message, state, all_photo, rand=ran, price=249)
    await db.new_count_order()
    await db.skin(ord, message=message)
    await message.answer(
        'Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы".')
    await message.answer('Кстати, все наши скины умеют моргать. 👀')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(state=cls.OrderSkin.additional_goods, content_types=['text'])
async def order_skin(message: types.Message):
    if message.text == 'Да':
        await message.answer("Какой предмет игрок чаще всего носит в руке? Конечно, "
                             "тотем бессмертия! Из него можно сделать абсолютно всё - от забавной статуэтки с "
                             "Вашим персонажем до магического кристалла")
        await message.answer("Сначала выберите, каким будет Ваш тотем - 2D или 3D", reply_markup=kb.type_totem_panel)
        await cls.OrderSkin.next()

    elif message.text == 'Нет':
        await message.answer("Хотите ли вы добавить к заказу плащ?", reply_markup=kb.agreement_panel)
        await cls.OrderSkin.cloak_description.set()

    elif message.text == 'Назад':
        await message.answer("Опишите, как Вы представляете Ваш будущий скин! "
                             "Чтобы оставить описание прежним введите 'Продолжить'", reply_markup=kb.cancel_panel)
        await cls.OrderSkin.description.set()


@dp.message_handler(state=cls.OrderSkin.totem_type, content_types=['text'])
async def order_skin(message: types.Message, state: FSMContext):
    if message.text == '2D' or message.text == '3D':
        item = message.text
        await state.update_data(
            {
                'totem_type': item
            }
        )
        await message.answer("Напишите, что Вы хотите видеть в качестве тотема.", reply_markup=kb.cancel_panel)
        await cls.OrderSkin.next()

    elif message.text == "Назад":

        await message.answer('Хотите ли Вы добавить к вашему заказу тотем?', reply_markup=kb.agreement_panel)
        await cls.OrderSkin.additional_goods.set()

    else:
        await message.answer("Выберете тип тотема!")


@dp.message_handler(state=cls.OrderSkin.totem_description, content_types=['text'])
async def order_skin(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" and message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        print(item)
        await state.update_data(
            {
                'totem_description': item
            }
        )

    if message.text != 'Назад' and not "'" in message.text and not '"' in message.text:
        await message.answer("Теперь приложите до 2 фотографий-референсов в формате "
                             ".jpeg или развёртку вашего скина в формате .png без сжатия, "
                             "фотографии лучше присылать отдельными сообщениями! Если вы не хотите прикреплять фото, "
                             "просто нажмите кнопку 'Продолжить'", reply_markup=kb.photo_panel)
        await cls.OrderSkin.next()

    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == "Назад":
        await message.answer("Выберите, каким будет Ваш тотем - 2D или 3D", reply_markup=kb.type_totem_panel)
        await cls.OrderSkin.totem_type.set()


@dp.message_handler(state=cls.OrderSkin.totem_photo, content_types=['document', 'photo', 'text'])
async def order_skin(message: types.Message, state: FSMContext):
    await order_photo(message, all_totem)

    if message.text == 'Продолжить':
        data = await state.get_data()
        description = data.get('totem_description')
        totem_type = data.get('totem_type')

        await message.answer(f"Описание тотема: {description},"
                             f"\nТип тотема: {totem_type}", reply_markup=kb.cancel_panel)

        if len(all_totem[message.from_user.id]) == 0:
            await message.answer("Вы не приложили файлы или фотографии")

        else:
            if len(all_totem[message.from_user.id]) > 3:
                await message.answer("Все фотографии или файлы больше двух были удалены!")
                del all_totem[message.from_user.id][2:]
            for i in all_totem[message.from_user.id]:
                try:
                    await bot.send_photo(message.chat.id, str(i))
                except:
                    pass
                try:
                    await bot.send_document(message.chat.id, str(i))
                except:
                    pass

        await message.answer('Хотите ли добавить плащ к вашему заказу?', reply_markup=kb.agreement_panel)

    elif message.text == 'Назад':
        await message.answer('Напишите, что Вы хотите видеть в качестве тотема. Если вы хотите оставить описание прежним введите "Продолжить"', reply_markup=kb.cancel_panel)
        await cls.OrderSkin.previous()

    elif message.text == 'Да':
        await message.answer("Майнкрафт предлагает ограниченное количество плащей, "
                             "да и получить их не так просто, но с помощью мода Advanced Capes Mod можно установить "
                             "плащ с совершенно любым рисунком! Мы сделаем его по Вашему описанию!")
        await message.answer("Опишите, как Вы представляете Ваш будущий плащ.", reply_markup=kb.cancel_panel)
        await cls.OrderSkin.cloak_description2.set()

    elif message.text == "Нет":
        await final_order(message, state)

    elif message.text == "Оплата":
        data = await state.get_data()
        totem_type = data.get('totem_type')

        if totem_type == '2D':
            await order_2(message, bot, 'скин', '2D тотем', 249, 49)
        elif totem_type == '3D':
            await order_2(message, bot, 'скин', '3D тотем', 249, 79)


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderSkin.totem_photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderSkin.totem_photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    data = await state.get_data()
    artist_name = data.get('artist')
    totem_type = data.get('totem_type')
    artist_id = data.get('artist_id')

    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    await db.new_count_order()
    ord = await get_ord_skin(message, state, all_photo, rand=ran, price=249)
    await db.skin(ord, message=message)
    if totem_type == '2D':
        ord_totem = await get_ord_other(message, state, all_totem, 'totem_description', artist_id, artist_name,
                                      totem_type=totem_type, rand=ran, price=49)
        await db.totem(ord_totem, message=message)
    if totem_type == '3D':
        ord_totem = await get_ord_other(message, state, all_totem, 'totem_description', artist_id, artist_name,
                                        totem_type=totem_type, rand=ran, price=79)
        await db.totem(ord_totem, message=message)
    await message.answer(
        'Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer('Кстати, все наши скины умеют моргать. 👀')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(state=cls.OrderSkin.cloak_description, content_types=['text'])
async def order_skin(message: types.Message):
    if message.text == 'Да':
        await message.answer("Майнкрафт предлагает ограниченное количество плащей, "
                             "да и получить их не так просто, но с помощью мода Advanced Capes Mod можно установить ")
        await message.answer("Опишите, как Вы представляете Ваш будущий плащ.", reply_markup=kb.cancel_panel)
        await cls.OrderSkin.cloak_description2.set()

    elif message.text == 'Назад':
        await message.answer('Хотите ли вы добавить к заказу тотем?', reply_markup=kb.agreement_panel)
        await cls.OrderSkin.additional_goods.set()

    elif message.text == 'Нет':
        await message.answer('Вы не выбрали дополнительные услуги, поэтому перейдём к оплате!')
        await order(message, bot, ord='Скин', price_1=249)


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderSkin.cloak_description)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderSkin.cloak_description, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    ord = await get_ord_skin(message, state, all_photo, rand=ran, price=249)
    await db.new_count_order()
    await db.skin(ord, message=message)
    await message.answer(
        'Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer('Кстати, все наши скины умеют моргать. 👀')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)


@dp.message_handler(state=cls.OrderSkin.cloak_description2, content_types=['text'])
async def order_skin(message: types.Message, state: FSMContext):
    if (message.text != "Продолжить" or message.text != 'Назад') and not ("'" in message.text or '"' in message.text):
        item = message.text
        print(item)
        await state.update_data(
            {
                'cloak_description': item
            }
        )

    if message.text != 'Назад' and not "'" in message.text and '"' not in message.text:
        await message.answer("Теперь приложите до 2 фотографий-референсов в формате "
                             ".jpeg или развёртку вашего скина в формате .png без сжатия, "
                             "фотографии лучше присылать отдельными сообщениями! Если вы не хотите прикреплять фото, "
                             "просто нажмите кнопку 'Продолжить'", reply_markup=kb.photo_panel)
        await cls.OrderSkin.cloak_photo.set()

    elif "'" in message.text or '"' in message.text:
        await message.answer("Уберите кавычки из текста!")

    elif message.text == "Назад":
        await message.answer('Хотите ли Вы добавить к вашему заказу плащ?', reply_markup=kb.agreement_panel)
        await cls.OrderSkin.previous()


@dp.message_handler(state=cls.OrderSkin.cloak_photo, content_types=['document', 'photo', 'text'])
async def order_skin(message: types.Message, state: FSMContext):
    await order_photo(message, all_cloak)

    if message.text == 'Продолжить':
        await final_order(message, state)

    elif message.text == 'Назад':
        await message.answer("Напишите, что Вы хотите видеть в качестве плаща.", reply_markup=kb.cancel_panel)
        await cls.OrderSkin.previous()

    elif message.text == "Оплата":
        data = await state.get_data()
        description_totem = data.get('totem_description')
        description_cloak = data.get('cloak_description')
        if not description_totem:
            await order_2(message, bot, 'скин', 'плащ', 249, 79)
        elif description_cloak and description_totem:
            data = await state.get_data()
            totem_type = data.get('totem_type')
            if totem_type == '2D':
                await order_3(message, bot, 'скин', '2D тотем', 'плащ', 249, 49, 79)
            elif totem_type == '3D':
                await order_3(message, bot, 'скин', '3D тотем', 'плащ', 249, 79, 79)


@dp.pre_checkout_query_handler(lambda query: True, state=cls.OrderSkin.cloak_photo)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(state=cls.OrderSkin.cloak_photo, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message, state: FSMContext):
    print('ОПЛАТА ПРОШЛА УСПЕШНО')
    data = await state.get_data()
    description_totem = data.get('totem_description')
    totem_type = data.get('totem_type')
    artist_name = data.get('artist')
    artist_id = data.get('artist_id')

    ran = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
    await db.new_count_order()

    ord = await get_ord_skin(message, state, all_photo, rand=ran, price=249)
    ord_cloak = await get_ord_other(message, state, all_cloak, 'cloak_description', artist_id, artist_name, rand=ran, price=79)

    await db.skin(ord, message=message)
    await db.cloak(ord_cloak, message=message)
    if description_totem:

        if totem_type == '2D':
            ord_totem = await get_ord_other(message, state, all_totem, 'totem_description', artist_id, artist_name,
                                           totem_type=totem_type, rand=ran, price=49)
            await db.totem(ord_totem, message=message)
        elif totem_type == '3D':
            ord_totem = await get_ord_other(message, state, all_totem, 'totem_description', artist_id, artist_name,
                                            totem_type=totem_type, rand=ran, price=79)
            await db.totem(ord_totem, message=message)

    await message.answer(
        'Оплата прошла успешно, художник вскоре начнёт работу! Посмотреть Ваши заказы можно в главном меню, раздел "Мои заказы"')
    await message.answer('Кстати, все наши скины умеют моргать. 👀')
    await message.answer(
        'Пока художник занимается Вашим заказом, можете посмотреть сериал, в котором используются скины и модели от нашей команды: https://www.youtube.com/playlist?list=PLVe49ImhHc6k2VwaXj-Hz6GRUU_nFyl16')
    await state.finish()
    await cmd_start(message)

@dp.message_handler(text='Мои заказы')
async def my_order(message: types.Message):
    await message.answer('Ваши заказы')
    keyboard = await kb.new_order_chat(message.from_user.id, 3)
    await message.answer(f'Кол-во ваших заказов {keyboard[0]}', reply_markup=keyboard[1])
    await cls.OrderChat.search.set()

num_cust = {}
id_art = {}
all_row = {}
id_cust = {}
@dp.message_handler(state=cls.OrderChat.search, content_types=['document', 'photo', 'text'])
async def cmd_text_order(message: types.Message, state: FSMContext):
    db = sq.connect('voxel.db')
    cur = db.cursor()
    cur.execute('SELECT NAME FROM sqlite_master WHERE TYPE="table"')
    all_current_tables = cur.fetchall()[1:7]
    if message.text != 'Назад':

        request = message.text.split()
        all_row[message.from_user.id] = []
        if request[0][1:] in [str(i) for i in range(0, 10000)] and request[0][0] == '№' and not message.text.isdigit(): #если вдруг у нас будет 10000 заказ, знай, в range лимит!!!

            num_cust[message.chat.id] = request[0][1:]
            for i in request[1:]:
                for table in all_current_tables:
                    result = cur.execute(f"SELECT * FROM {table[0]}")
                    print(request[0][1:])
                    for row in result:
                        if row[2] == i and str(row[1]) == request[0][1:]:
                            await message.answer(f"Ваше описание на {row[2]}: {row[-3]}")
                            if row[2] == 'скин' or row[2] == 'тотем':
                                await message.answer(f"Тип: {row[-5]}")
                            all_file = str(row[-2])[1:-1].replace("'", "").replace(',', '').split()
                            for file in all_file:
                                try:
                                    await bot.send_photo(message.chat.id, file)
                                except:
                                    await bot.send_document(message.chat.id, file)
                            id_art[message.from_user.id] = row[4]

                            all_row[message.from_user.id].append(row)

            await message.answer('Вы хотите открыть чат с художником?', reply_markup=kb.agreement_chat_panel)
            await cls.OrderChat.pre_chat.set()
        else:
            await message.answer('Введите корректный заказ. Если вы хотите выйти из панели заказчика введите "Назад",'
                                 ' либо нажмите соответствующую кнопку')
    else:
        await state.finish()
        await cmd_start(message)


@dp.message_handler(state=cls.OrderChat.pre_chat, content_types=['text'])
async def cmd_text_order(message: types.Message):
    keyboard = await kb.new_order_chat(message.from_user.id, 3)
    if message.text == 'Да':
        await message.answer(f'Открыт чат с художником номер {num_cust[message.from_user.id]}\nЧтобы выйти из чата впишите "Выйти",'
                             f' либо нажмиите соответствующую кнопку. Пока вы находитесь в чате,'
                             f' все ваши сообщение отправляются заказчику, будьте внимательны!',
                             reply_markup=kb.exit_ord_panel)
        print(all_row[message.from_user.id])
        await cls.OrderChat.chat.set()

    elif message.text == "Назад":
        await message.answer(f'Кол-во ваших заказов {keyboard[0]}', reply_markup=keyboard[1])
        await cls.OrderChat.search.set()

    else:
        await message.answer('Выберите действие!')


@dp.message_handler(state=cls.OrderChat.chat, content_types=['document', 'photo', 'text'])
async def cmd_text_order(message: types.Message):
    keyboard = await kb.new_order_chat(message.from_user.id, 3)

    if message.text == 'Выйти':
        await message.answer('Вы вышли из чата!', reply_markup=keyboard[1])
        await cls.OrderChat.search.set()

    elif message.text == "Завершить заказ":
        await message.answer('Вы уверены? Чтобы завершить заказ напишите: `ЗАВЕРШИТЬ ЗАКАЗ`', parse_mode="MARKDOWN", reply_markup=kb.cancel_panel)
        await cls.OrderChat.final_chat.set()

    elif message.photo:
        try:
            documents_id = message.photo[2].file_id

        except IndexError:
            documents_id = message.photo[0].file_id

        await message.bot.send_photo(id_art[message.from_user.id], documents_id, caption=f'Сообщение заказчика №{num_cust[message.from_user.id]}: {message.caption}')
        await message.answer('Ваше сообщение было отправлено! ✉️')

    elif message.text:
        await message.bot.send_message(id_art[message.from_user.id], f'Сообщение заказчика №{num_cust[message.from_user.id]}:\n{message.text}')
        await message.answer('Ваше сообщение было отправлено! ✉️')

    elif message.document:
        try:
            documents_id = message.document.file_id
            await message.bot.send_document(id_art[message.from_user.id], documents_id, caption=f'Сообщение заказчика №{num_cust[message.from_user.id]}: {message.caption}')
            await message.answer('Ваше сообщение было отправлено! ✉️')
        except:
            await message.answer('Сообщение не было отправлено, возникла ошибка!')


@dp.message_handler(state=cls.OrderChat.final_chat, content_types=['text'])
async def cmd_text_order(message: types.Message, state: FSMContext):
    keyboard = await kb.new_order_chat(message.from_user.id, 3)
    if message.text == "Назад":
        await message.answer(f'Кол-во ваших заказов {keyboard[0]}', reply_markup=keyboard[1])
        await cls.OrderChat.search.set()
    elif message.text == 'ЗАВЕРШИТЬ ЗАКАЗ':
        for ord in all_row[message.from_user.id]:
            if ord[2] == '4D_Скин':
                await db.skin_4d(ord, var=2, message=message)
                await db.skin_4d(ord[1], var=3, message=message)
            elif ord[2] == 'скин':
                await db.skin(ord, var=2, message=message)
                await db.skin(ord[1], var=3, message=message)
            elif ord[2] == 'аватар':
                await db.avatar(ord, var=2, message=message)
                await db.avatar(ord[1], var=3, message=message)
            elif ord[2] == 'плащ':
                await db.cloak(ord, var=2, message=message)
                await db.cloak(ord[1], var=3, message=message)
            elif ord[2] == 'тотем':
                await db.totem(ord, var=2, message=message)
                await db.totem(ord[1], var=3, message=message)

        await bot.send_message(ord[4], f'Покупатель №{ord[1]} завершил заказ!')
        await message.answer('Заказ завершён!', reply_markup=kb.menu)
        await state.finish()

@dp.message_handler(text="Заказы")
async def cmd_text_artist(message: types.Message):
    if str(message.from_user.id) in db.get_artists_info():
        keyboard = await kb.new_order_chat(message.from_user.id, 4)
        await message.answer(f'Кол-во ваших заказов {keyboard[0]}', reply_markup=keyboard[1])
        await cls.ArtistPanel.search.set()
    else:
        await message.reply("Извините, я вас не понимаю. 😔")


@dp.message_handler(state=cls.ArtistPanel.search, content_types=['document', 'photo', 'text'])
async def cmd_text_artist(message: types.Message, state: FSMContext):
    db = sq.connect('voxel.db')
    cur = db.cursor()
    cur.execute('SELECT NAME FROM sqlite_master WHERE TYPE="table"')
    all_current_tables = cur.fetchall()[1:7]
    if message.text != 'Назад':

        request = message.text.split()

        if request[0][1:] in [str(i) for i in range(0, 10000)] and request[0][0] == '№' and not message.text.isdigit():

            num_cust[message.from_user.id] = request[0][1:]
            for i in request[1:]:
                for table in all_current_tables:
                    result = cur.execute(f"SELECT * FROM {table[0]}")
                    for row in result:
                        if row[2] == i and str(row[1]) == request[0][1:]:
                            await message.answer(f"Описание заказчика на {row[2]}: {row[-3]}")
                            if row[2] == 'скин' or row[2] == 'тотем':
                                await message.answer(f"Тип: {row[-5]}")
                            all_file = str(row[-2])[1:-1].replace("'", "").replace(',', '').split()
                            for file in all_file:
                                try:
                                    await bot.send_photo(message.chat.id, file)
                                except:
                                    await bot.send_document(message.chat.id, file)
                            id_cust[message.from_user.id] = row[3]

            await message.answer('Вы хотите открыть чат с заказчиком?', reply_markup=kb.agreement_chat_panel)
            await cls.ArtistPanel.pre_chat.set()
        else:
            await message.answer('Введите корректный заказ. Если вы хотите выйти из панели художника введите "Назад",'
                                 ' либо нажмите соответствующую кнопку')
    else:
        await state.finish()
        await cmd_start(message)


@dp.message_handler(state=cls.ArtistPanel.pre_chat, content_types=['text'])
async def cmd_text_artist(message: types.Message):
    keyboard = await kb.new_order_chat(message.from_user.id, 4)
    if message.text == 'Да':
        await message.answer(f'Открыт чат с заказчиком номер {num_cust[message.from_user.id]}\nЧтобы выйти из чата впишите "Выйти",'
                             f' либо нажмиите соответствующую кнопку, пока вы находитесь в чате,'
                             f' все ваши сообщение отправляются заказчику, будьте внимательны!',
                             reply_markup=kb.exit_panel)
        await cls.ArtistPanel.chat.set()

    elif message.text == "Назад":
        await message.answer(f'Кол-во ваших заказов {keyboard[0]}', reply_markup=keyboard[1])
        await cls.ArtistPanel.search.set()
    else:
        await message.answer('Выберите действие!')


@dp.message_handler(state=cls.ArtistPanel.chat, content_types=['document', 'photo', 'text'])
async def cmd_text_artist(message: types.Message):
    keyboard = await kb.new_order_chat(message.from_user.id, 4)

    if message.text == 'Выйти':
        await message.answer('Вы вышли из чата!', reply_markup=keyboard[1])
        await cls.ArtistPanel.search.set()

    elif message.photo:
        try:
            documents_id = message.photo[2].file_id

        except IndexError:
            documents_id = message.photo[0].file_id

        await message.bot.send_photo(id_cust[message.from_user.id], documents_id, caption=f'Сообщение от художника заказа №{num_cust[message.from_user.id]}')
        await message.answer('Ваше сообщение было отправлено! ✉️')

    elif message.text:
        await message.bot.send_message(id_cust[message.from_user.id], f'Сообщение от художника заказа №{num_cust[message.from_user.id]}:\n{message.text}')
        await message.answer('Ваше сообщение было отправлено! ✉️')

    elif message.document:
        try:
            documents_id = message.document.file_id
            await message.bot.send_document(id_cust[message.from_user.id], documents_id, caption=f'Сообщение от художника заказа №{num_cust[message.from_user.id]}')
            await message.answer('Ваше сообщение было отправлено! ✉️')
        except:
            await message.answer('Сообщение не было отправлено, возникла ошибка!')


@dp.message_handler(text='Панель администрации')
async def cmd_text_admins(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы вошли в панель Администрации', reply_markup=kb.admins_panel)
    else:
        await message.reply("Извините, я вас не понимаю. 😔")


@dp.message_handler(text="Панель художника")
async def cmd_text_artist(message: types.Message):
    if str(message.from_user.id) in db.get_artists_info():
        await message.answer('Выберете действие', reply_markup=kb.artist_personal_panel)
    else:
        await message.reply("Извините, я вас не понимаю. 😔")


@dp.message_handler(text="Баланс")
async def cmd_text_artist(message: types.Message):
    if str(message.from_user.id) in db.get_artists_info():
        money = await kb.get_money(message.from_user.id) // 2
        await message.answer(f'Ваш баланс: {money} рублей! Мы выплачиваем деньги сотрудникам первого числа каждого месяца')
    else:
        await message.reply("Извините, я вас не понимаю. 😔")



@dp.message_handler()
async def answer(message: types.Message):
    await message.reply("Извините, я вас не понимаю. 😔")
