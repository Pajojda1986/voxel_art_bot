from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderSkin(StatesGroup):

    type = 'skin'
    hand_type = State()
    artist = State()
    description = State()
    photo = State()
    additional_goods = State()
    totem_type = State()
    totem_description = State()
    totem_photo = State()
    cloak_description = State()
    cloak_description2 = State()
    cloak_photo = State()
    payment_skin = State()

class OrderSkin4D(StatesGroup):
    type_ord = 'skin4d'
    description = State()
    photo = State()
    email = State()
    payment = State()

class OrderCloak(StatesGroup):

    type_ord = 'cloak'
    description = State()
    photo = State()
    payment = State()


class Order3dAvatar(StatesGroup):

    type_ord = 'avatar'
    description = State()
    photo = State()
    payment = State()

class OrderTotem(StatesGroup):

    type_ord = 'totem'
    type = State()
    description = State()
    photo = State()
    payment = State()

class OrderChat(StatesGroup):
    search = State()
    pre_chat = State()
    chat = State()
    final_chat = State()


class ArtistPanel(StatesGroup):

    search = State()
    pre_chat = State()
    chat = State()


class AdminsPanel(StatesGroup):

    search = State()
    close = State()