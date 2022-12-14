import json
import time

from bestchange_api import BestChange
import asyncio


def run_bestchange_exchange():
    time.sleep(20)
    asyncio.Task(run_bestchange_exchange1())



async def run_bestchange_exchange1():
    try:
        await asyncio.get_event_loop().run_in_executor(None, update_exchangers)
    except:
        print("out exch")
        run_bestchange_exchange()


def update_exchangers():
    while True:
        print("Started hearing")
        api = BestChange()
        temp_dict = {}
        exchangers = api.exchangers().get()
        with open("exchangers.json", 'r') as f:
            temp_dict = json.load(f)
        print("start len", len(temp_dict))
        for i in exchangers:
            data = exchangers[i]
            temp_dict[data['name']] = data['id']
        with open("exchangers.json", 'w') as f:
            json.dump(temp_dict, f)
        print("end len", len(temp_dict))
        time.sleep(120)
