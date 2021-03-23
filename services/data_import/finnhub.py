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

symbols = ['tlry', 'rkt', 'out', 'amc', 'wkhs', 'siri', 'iag', 'srne', 'BINANCE:BTCUSDT']

def on_message(ws, message):
    # Look at the message type during the market open
    # {type: ping}
    # {"data":
    # [
    # {"c":null,"p":57733.37,"s":"BINANCE:BTCUSDT","t":1616396091995,"v":0.002135},
    # {"c":null,"p":57733.37,"s":"BINANCE:BTCUSDT","t":1616396091995,"v":0.00218},
    # {"c":null,"p":57733.37,"s":"BINANCE:BTCUSDT","t":1616396092049,"v":0.01155},
    # {"c":null,"p":57735.62,"s":"BINANCE:BTCUSDT","t":1616396092049,"v":0.003651},
    # {"c":null,"p":57735.64,"s":"BINANCE:BTCUSDT","t":1616396092049,"v":0.013429},
    # {"c":null,"p":57736.38,"s":"BINANCE:BTCUSDT","t":1616396092089,"v":0.000468},{"c":null,"p":57736.38,"s":"BINANCE:BTCUSDT","t":1616396092115,"v":0.009987},{"c":null,"p":57736.38,"s":"BINANCE:BTCUSDT","t":1616396092145,"v":0.004421},{"c":null,"p":57736.38,"s":"BINANCE:BTCUSDT","t":1616396092150,"v":0.153067},{"c":null,"p":57736.38,"s":"BINANCE:BTCUSDT","t":1616396092171,"v":0.036148}],
    # "type":"trade"}
    msg = json.loads(message)
    if msg["type"] == "trade":
        for trade in msg["data"]:
            # ok now I can publish to the kafka
            if trade["v"] > 0.01:
                print(f"ticker: {trade['s']}, last price: {trade['p']}, volume: {trade['v']}")
    else:
        print("received something else")
        print(message)


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

