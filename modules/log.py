import pandas as pd
import asyncio
import threading
from time import sleep
from datetime import datetime, time
from modules import api


class logVars:
    active = False


async def _Start():

    while True:
        if not logVars.active:
            sleep(1)
            continue

        for cp in ['CALL', 'PUT']:
            for strikeRange in ['ITM', 'OTM']:
                temp_list = []
                temp_dict = api.options.chains("$SPX", contractType = cp, range = strikeRange).json()
                for value in temp_dict['callExpDateMap'].values():
                    for quote in value.values():
                        row = quote[0]
                        row['underlyingPrice'] = temp_dict['underlyingPrice']
                        temp_list.append(row)
                for value in temp_dict['putExpDateMap'].values():
                    for quote in value.values():
                        row = quote[0]
                        row['underlyingPrice'] = temp_dict['underlyingPrice']
                        temp_list.append(row)
                temp_df = pd.DataFrame(temp_list)[['putCall', 
                                                   'bid', 
                                                   'ask', 
                                                   'last', 
                                                   'bidSize', 
                                                   'askSize', 
                                                   'volatility',
                                                   'delta', 
                                                   'gamma', 
                                                   'theta', 
                                                   'vega', 
                                                   'rho', 
                                                   'openInterest', 
                                                   'timeValue', 
                                                   'strikePrice', 
                                                   'expirationDate', 
                                                   'daysToExpiration', 
                                                   'lastTradingDay', 
                                                   'totalVolume',
                                                   'tradeTimeInLong', 
                                                   'quoteTimeInLong',
                                                   'underlyingPrice',
                                                   'intrinsicValue', 
                                                   'extrinsicValue']]
                temp_df.to_csv('log.csv', mode='a', index=False)


def startManual():
    def start():
        asyncio.run(_Start())

    thread = threading.Thread(target=start).start()


def startAutomatic(streamAfterHours=False, streamPreHours=False):
    start = time(9, 29, 0)
    end = time(16, 1, 0)
    if streamPreHours:
        start = time(8, 0, 0)
    if streamAfterHours:
        end = time(20, 0, 0)

    def checker():
        def _inHours():
            return (start <= datetime.now().time() <= end) and (0 <= datetime.now().weekday() <= 4)

        while True:
            if _inHours() and not logVars.active:
                logVars.active = True
                startManual()
            elif not _inHours() and logVars.active:
                logVars.active = False
            sleep(60)

    threading.Thread(target=checker).start()

