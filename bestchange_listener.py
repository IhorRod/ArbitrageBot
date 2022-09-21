import asyncio
import time
import config
from config import *
from bestchange_api import BestChange
import math
from numba import njit


def run_bestchange():
    asyncio.Task(run_bestchange1())


async def run_bestchange1():
    await asyncio.get_event_loop().run_in_executor(None, update_cots)

@njit(cache=True, fastmath=True)
def calculate(value: float, give: float, get: float, from_cot: float, to_cot: float):
    volume_from = value / from_cot
    volume_to = (volume_from / give) * get
    value1 = volume_to * to_cot
    return value1, volume_from, volume_to


def update_cots():
    while True:
        config.list_bestchange = get_cots()
        if len(config.list_bestchange)>5:
            config.list_bestchange = config.list_bestchange[:5]


def get_cots():
    print("start")
    start_time = time.time()
    api = BestChange()
    print("finish in", time.time() - start_time)
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

                        temp_calc = calculate(float(parameters['value']),float(k['give']), float(k['get']), quotes[from_cot][1], quotes[to_cot][2])

                        abs_diff = round(temp_calc[0], 2)
                        diff = round(((abs_diff / float(parameters['value'])) - 1) * 100, 1)
                        # print(i, j, diff, abs_diff)
                        if diff >= parameters['min_spread']:
                            check = True
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
                                    'to_val': temp_calc[2]
                                }
                            )
    lst_temp.sort(key=lambda x: -x['spread_abs'])
    return lst_temp
