from aiogram import Bot
from aiogram.types import Message, LabeledPrice
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('PAYMENTS_TOKEN')

async def order(message: Message, bot: Bot, ord, price_1):
    if token.split(':')[1] == 'TEST':
        await message.answer("ЭТО ТЕСТОВЫЙ ПЛАТЁЖ")
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=ord,
        description=f'Уникальный {ord} на заказ',
        payload='Payment thought a bot',
        provider_token=token,
        currency='rub',
        prices=[
            LabeledPrice(
                label=ord,
                amount=price_1 * 100
            ),
        ],
        start_parameter='VoxelArt_bot',
        need_email=True,
        send_email_to_provider=True,
        protect_content=True,
    )

async def order_2(message: Message, bot: Bot, ord_1, ord_2, price_1, price_2):
    if token.split(':')[1] == 'TEST':
        await message.answer("ЭТО ТЕСТОВЫЙ ПЛАТЁЖ")
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=f'{ord_1} и {ord_2}',
        description=f'Уникальный {ord_1} и {ord_2} на заказ',
        payload='Payment thought a bot',
        provider_token=token,
        currency='rub',
        prices=[
            LabeledPrice(
                label=ord_1,
                amount=price_1 * 100
            ),
            LabeledPrice(
                label=ord_2,
                amount=price_2 * 100
            ),
        ],
        start_parameter='VoxelArt_bot',
        send_email_to_provider=True,
        protect_content=True,
    )

async def order_3(message: Message, bot: Bot, ord_1, ord_2, ord_3, price_1, price_2, price_3):
    if token.split(':')[1] == 'TEST':
        await message.answer("ЭТО ТЕСТОВЫЙ ПЛАТЁЖ")
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=f'{ord_1}, {ord_2} и {ord_3}',
        description=f'Уникальный {ord_1} и {ord_2}, а также {ord_3} на заказ',
        payload='Payment thought a bot',
        provider_token=token,
        currency='rub',
        prices=[
            LabeledPrice(
                label=ord_1,
                amount=price_1 * 100
            ),
            LabeledPrice(
                label=ord_2,
                amount=price_2 * 100
            ),
            LabeledPrice(
                label=ord_3,
                amount=price_3 * 100
            ),
        ],
        start_parameter='VoxelArt_bot',
        send_email_to_provider=True,
        protect_content=True,
    )
