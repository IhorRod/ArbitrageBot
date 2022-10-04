import asyncio
from binance import AsyncClient, BinanceSocketManager
from config import *

async def main():
    while True:
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        ts = bm.book_ticker_socket()

        async with ts as tscm:
            while True:
                res = await tscm.recv()
                if res['s'] in quotes:
                    quotes[res['s']] = (quotes[res['s']][0], float(res['b']), float(res['a']))
                    print(res)


def start_listening():
    asyncio.Task(main())
