import time

from config import *
from bestchange_api import BestChange
import math


def calculate(give: float, get: float, from_cot: str, to_cot: str):
    value = float(parameters['value'])
    value1 = (value/quotes[from_cot][1]/give)*get*quotes[to_cot][2]
    return value1

def get_cots():
    print("start")
    start_time = time.time()
    api = BestChange()
    print("finish in", time.time()-start_time)
    lst_temp = []
    for i in quotes:
        for j in quotes:
            if i != j and quotes[i][1] != 0 and quotes[j][1] != 0:
                cots = api.rates().filter(
                    quotes[i][0],
                    quotes[j][0]
                )
                check = False
                for k in cots:
                    reviews = str(k['reviews']).split('.')
                    if int(reviews[0]) <= parameters['max_bad'] and int(reviews[1]) >= parameters[
                        'min_good'] and not check:

                        abs_diff = calculate(float(k['give']), float(k['get']), i, j)
                        diff = ((abs_diff/float(parameters['value']))-1)*100
                        #print(i, j, diff, abs_diff)
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
                                }
                            )
    lst_temp.sort(key=lambda x: x[2])
    return lst_temp
