import uuid
import os
from dotenv import load_dotenv
from yookassa import Configuration, Payment

load_dotenv()
token = os.getenv('PAYMENTS_URL_TOKEN')
id = os.getenv('PAYMENTS_ID')

Configuration.account_id = 'test_il8UG1ALNxtxlDhuMINvZ_044hUboZRdoglwuf3u68w'
Configuration.secret_key = '232272'

payment = Payment.create({
    "amount": {
        "value": "399.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://web.telegram.org/k/#@VoxelArt_bot"
    },
    "capture": True,
    "description": "Заказ №1"
}, uuid.uuid4())
print(payment)
