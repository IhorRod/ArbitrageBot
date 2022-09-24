import asyncio
import time
import config
from config import *
from bestchange_api import BestChange
from numba import njit
import numpy as np


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
        print("finish all in", time.time() - start_time_all)
        print(config.list_bestchange)


def get_cots():
    start_time = time.time()
    api = BestChange()
    print("finish connect in", time.time() - start_time)
    lst_temp = []
    new_quotes = [(k, v[0], v[1], v[2]) for k, v in quotes.items() if v[1] != 0 and k not in quotes_black]
    pairs = np.array(
        [(k1, k2) for k1 in new_quotes for k2 in new_quotes if k1[0] != k2[0]])

    for i in pairs:
        cots = api.rates().filter(
            i[0][1],
            i[1][1]
        )
        check = False
        for k in cots:
            reviews = str(k['reviews']).split('.')
            if int(reviews[0]) <= parameters['max_bad'] \
                    and int(reviews[1]) >= parameters['min_good'] \
                    and not check \
                    and k['exchange_id'] not in exchangers_black:

                temp_calc = calculate(float(parameters['value']), float(k['give']), float(k['get']),
                                      i[0][2], i[1][3])

                abs_diff = round(temp_calc[0], 2)
                diff = round(((abs_diff / float(parameters['value'])) - 1) * 100, 1)
                # print(i, j, diff, abs_diff)
                if diff >= parameters['min_spread']:
                    check = True
                    lst_temp.append(
                        {
                            'from': i[0][0][:-4],
                            'to': i[1][0][:-4],
                            'spread_abs': abs_diff,
                            'spread_proc': diff,
                            'link': "https://www.bestchange.ru/click.php?id={}&from={}&to={}&city=0"
                            .format(k["exchange_id"], k["give_id"], k["get_id"]),
                            'buy': i[0][2],
                            'sell': i[1][3],
                            'give': k['give'],
                            'get': k['get'],
                            'from_val': temp_calc[1],
                            'to_val': temp_calc[2]
                        }
                    )

    lst_temp.sort(key=lambda x: -x['spread_abs'])
    return lst_temp
