import time

from config import *
from bestchange_api import BestChange
import math


def calculate(give: float, get: float, from_cot: str, to_cot: str):
    value = float(parameters['value'])
    value1 = (value/quotes[from_cot][1]/give)*get*quotes[to_cot][2]
    return (value1-value)/value*100

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
                    quotes[i][0]
                )
                check = False
                for k in cots:
                    reviews = str(k['reviews']).split('.')
                    if int(reviews[0]) <= parameters['max_bad'] and int(reviews[1]) >= parameters[
                        'min_good'] and not check:
                        diff = calculate(float(k['give']), float(k['get']), i, j)
                        print(i, j, diff)
                        if diff >= parameters['min_spread']:
                            check = True
                            lst_temp.append(
                                (i[:-4], j[:-4], diff)
                            )
    return lst_temp
