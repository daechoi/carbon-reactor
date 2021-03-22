# allows real-time quotes in addition to fundamental static data.

# I am going to use tiblio to see what's interesting in the universe of markets.
# # Then use finnhub to subscribe to events for technical/fundamental analysis.

# Use the 
# Should look at samuraioption and tradier

# This stuff interests me.
# Do papertrading and backdate testing on the strategy

import websocket
import json
from const import CONST

symbols = ['tlry', 'rkt', 'out', 'amc', 'wkhs', 'siri', 'iag', 'srne']

def on_message(ws, message):
    print("received: " + message)


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("##### Closed #####")

def on_open(ws):
    for symbol in symbols:
        request_data = {
                "type": "subscribe",
                "symbol": str(symbol)
                }
        ws.send(json.dumps(request_data))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(CONST.URL_FINNHUB_WS_API+"?token="+CONST.FINHUB_API,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
            )
    ws.on_open = on_open
    ws.run_forever()

