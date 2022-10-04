import asyncio
import time
import config
from config import *
from bestchange_api import BestChange
from numba import njit
import numpy as np
import traceback
import json


def run_bestchange():
    time.sleep(10)
    asyncio.Task(run_bestchange1())


async def run_bestchange1():
    try:
        await asyncio.get_event_loop().run_in_executor(None, update_cots)
    except:
        run_bestchange()


@njit(cache=True)
def calculate(value: float, give: float, get: float, from_cot: float, to_cot: float):
    volume_from = value / from_cot
    volume_to = (volume_from / give) * get
    value1 = volume_to * to_cot
    return value1, volume_from, volume_to


def update_cots():
    while True:
        print("start")
        start_time_all = time.time()
        config.list_bestchange = get_cots()
        if len(config.list_bestchange)>20:
            config.list_bestchange = config.list_bestchange[:20]
        print("finish all in", time.time() - start_time_all)
        print(config.list_bestchange)


def get_cots():
    start_time = time.time()
    api = BestChange()
    print("finish connect in", time.time() - start_time)
    lst_temp = []
    
    for i in quotes:
        for j in quotes:
            if i != j \
                    and quotes[i][1] != 0 \
                    and quotes[j][1] != 0 \
                    and i not in quotes_black \
                    and j not in quotes_black:
                cots = api.rates().filter(
                    quotes[i][0],
                    quotes[j][0]
                )
                check = False
                for k in cots:
                    reviews = str(k['reviews']).split('.')
                    if int(reviews[0]) <= parameters['max_bad'] \
                            and int(reviews[1]) >= parameters['min_good'] \
                            and not check \
                            and k['exchange_id'] not in exchangers_black:
                        temp_calc = calculate(float(parameters['value']),float(k['give']), float(k['get']), quotes[i][1], quotes[j][2])
                        abs_diff = round(temp_calc[0], 2)
                        diff = round(((abs_diff / float(parameters['value'])) - 1) * 100, 1)
                        # print(i, j, diff, abs_diff)
                        if diff >= parameters['min_spread'] and temp_calc[1]>=k['min_sum'] and temp_calc[1]<=k['max_sum']:
                            check = True
                            with open("exchangers.json", "r") as read_file:
                                exchangers_names: dict = json.load(read_file)
                            for f in exchangers_names:
                                if int(exchangers_names[f]) == k["exchange_id"]:
                                    exch_name: str = f
                            lst_temp.append(
                                {
                                    'from': i[:-4],
                                    'to': j[:-4],
                                    'spread_abs': abs_diff,
                                    'spread_proc': diff,
                                    'link': "https://www.bestchange.ru/click.php?id={}&from={}&to={}&city=0"
                                    .format(k["exchange_id"], k["give_id"], k["get_id"]),
                                    'buy': quotes[i][1],
                                    'sell': quotes[j][2],
                                    'give': k['give'],
                                    'get': k['get'],
                                    'from_val': temp_calc[1],
                                    'to_val': temp_calc[2],
                                    'exch_name': exch_name
                                }
                            )

    lst_temp.sort(key=lambda x: -x['spread_abs'])
    
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
    
    return lst_temp
