import os
import json
API_TOKEN = os.environ.get("API_TOKEN")
with open('config.json') as json_file:
    parameters: dict = json.load(json_file)

list_bestchange = []
exchangers_black = {}
quotes_black = []

quotes = {
    "LUNAUSDT": (2, 0, 0),
    "OMGUSDT": (48, 0, 0),
    "BNBUSDT": (19, 0, 0),
    "BATUSDT": (61, 0, 0),
    "NEARUSDT": (76, 0, 0),
    "SOLUSDT": (82, 0, 0),
    "BTCUSDT": (93, 0, 0),
    "LTCUSDT": (99, 0, 0),
    "ICXUSDT": (104, 0, 0),
    "DOGEUSDT": (115, 0, 0),
    "XVGUSDT": (124, 0, 0),
    "WAVESUSDT": (133, 0, 0),
    "KMDUSDT": (134, 0, 0),
    "ONTUSDT": (135, 0, 0),
    "MATICUSDT": (138, 0, 0),
    "ETHUSDT": (139, 0, 0),
    "DASHUSDT": (140, 0, 0),
    "XMRUSDT": (149, 0, 0),
    "XRPUSDT": (161, 0, 0),
    "ZECUSDT": (162, 0, 0),
    "XTZUSDT": (175, 0, 0),
    "NEOUSDT": (177, 0, 0),
    "EOSUSDT": (178, 0, 0),
    "ADAUSDT": (181, 0, 0),
    "XLMUSDT": (182, 0, 0),
    "TRXUSDT": (185, 0, 0),
    "SHIBUSDT": (32, 0, 0),
    "LINKUSDT": (197, 0, 0),
    "ATOMUSDT": (198, 0, 0),
    "DOTUSDT": (201, 0, 0),
    "UNIUSDT": (202, 0, 0),
    "DAIUSDT": (203, 0, 0),
    "TONUSDT": (209, 0, 0),
    "MKRUSDT": (213, 0, 0),
    "ALGOUSDT": (216, 0, 0),
    "AVAXUSDT": (217, 0, 0),
}
