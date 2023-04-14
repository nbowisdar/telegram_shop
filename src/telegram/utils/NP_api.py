import asyncio
import json
from pprint import pprint

from setup import BASE_URL_NP, NOVA_POST
import aiohttp


async def check_city_np_exist(city: str) -> bool:
    body = {
        "apiKey": NOVA_POST,
        "modelName": "Address",
        "calledMethod": "searchSettlements",
        "methodProperties": {
            "CityName": city,
            "Limit": "50",
            "Page": "2"
        }
    }
    async with aiohttp.ClientSession() as client:
        async with client.post(BASE_URL_NP, json=body) as resp:
            resp_j = await resp.json()
            if resp_j['success'] == False:
                return False
            if resp_j['data'][0]["TotalCount"]:
                return True
            return False


async def get_np_address(city: str, n: str) -> bool:
    body = {
        "apiKey": NOVA_POST,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityName": city,
            "Page": "1",
            "Limit": "50",
            "Language": "UA",
            "WarehouseId": n
        }
    }
    async with aiohttp.ClientSession() as client:
        async with client.post(BASE_URL_NP, json=body) as resp:
            resp_j = await resp.json()
            if resp_j['data']:
                return resp_j['data'][0]["Description"] #  .replace("'", "")
            else:
                return False


async def test():
    # x = await check_city_np_exist("дн1епр")
    # print(x)

    a = await get_np_address("днепр", "28")
    print(a)

# asyncio.run(test())
