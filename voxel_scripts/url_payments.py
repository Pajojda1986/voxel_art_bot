import uuid
import os
from dotenv import load_dotenv
from yookassa import Configuration, Payment

load_dotenv()
token = os.getenv('PAYMENTS_URL_TOKEN')
id = os.getenv('PAYMENTS_ID')

Configuration.account_id = id
Configuration.secret_key = token


async def get_url_payment(amount, desc, email_):
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://web.telegram.org/k/#@VoxelArt_bot"
        },
        "capture": True,
        "description": desc,
        "receipt": {
            "customer": {
                "email": email_
            },
            "items": [
                {
                    "description": desc,
                    "vat_code": 1,
                    "quantity": "1",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                }
            ]
        }
    }, uuid.uuid4())

    return payment

