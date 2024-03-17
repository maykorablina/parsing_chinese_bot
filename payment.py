import json
import hashlib
import base64

from aiohttp import ClientSession

from functions import MERCHANT_ID

def generate_headers(data):
    json_dumps = json.dumps(data)
    sign = hashlib.md5(
        base64.b64encode(json_dumps.encode("ascii")) + API_KEY.encode("ascii")
    ).hexdigest()

    return {"merchant": MERCHANT_ID, "sign": sign, "content-type": "application/json"}

async def create_invoice(user_id):
    async with ClientSession() as session:
        data = {
            "amount": "10",
            "order_id": f"MY-TEST-ORDER-{user_id}-000",
            "currency": "USDT",
            "network": "tron",
            "lifetime": 900
        }

        json_dumps = json.dumps(data)

        response = await session.post(
            "https://api.cryptomus.com/v1/payment",
            data=data,
            headers=generate_headers(data)
        )
