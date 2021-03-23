import threading
import json
from kafka.consumer.group import KafkaConsumer
import websocket
from const import CONST
import time
from kafka import KafkaProducer

class FinStreamer(threading.Thread):
    def __init__(self, symbols):
        threading.Thread.__init__(self)
        self.symbols = symbols
        self.daemon = True
        self.producer = KafkaProducer(
                value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                bootstrap_servers=CONST.KAFKA_BROKER
                )

    def run(self):

        # Running the run_forever() in a seperate thread.
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(CONST.URL_FINNHUB_WS_API+"?token="+CONST.FINHUB_API,
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def send(self, data):

        # Wait till websocket is connected.
        while not self.ws.sock.connected:
            time.sleep(0.25)

        print ('Sending data...'+ data)
        self.ws.send("Hello %s" % data)

    def stop(self):
        print ('Stopping the websocket...')
        self.ws.keep_running = False
        self.ws.close()

    def on_message(self, ws, message):
        msg = json.loads(message)
        if msg["type"] == "trade":
            for trade in msg["data"]:
                # ok now I can publish to the kafka
#                if trade["v"] > 0.01:
#                print(f"ticker: {trade['s']}, last price: {trade['p']}, volume: {trade['v']}, condition: {trade['c']}, timestamp: {trade['t']}")
                self.producer.send(CONST.TOPIC_TRADES, value=trade)
#                self.producer.flush()

        else:
            print("received something else")
            print(message)

    def on_error(self, ws, error):
        print (error)
        if ws is not None:
            self.stop()

        while True:
            try:
                time.sleep(10)
                if not self.is_alive():
                    self.start()
                else:
                    self.stop()
                    self.run()

            except Exception as e:
                print(f"Restart failed: {e}")


    def on_close(self, ws):
        print ('#### Closed connection ####')

    def on_open(self, ws):
        for symbol in self.symbols:
            request_data = {
                    "type": "subscribe",
                    "symbol": str(symbol)
                    }
            ws.send(json.dumps(request_data))


if __name__ == "__main__":

    # Reload the FinStreamer if the symbols change
    symbols = ['TLRY', 'RKT', 'OUT', 'AMC', 'WKHS', 'SIRI', 'IAG', 'SRNE', 'EC', 'TSLA', 'GME', 'AAPL', 'BINANCE:BTCUSDT']
    iex = FinStreamer(symbols)
    iex.start()

    consumer = KafkaConsumer(
            CONST.TOPIC_LONG_CALLS_PUTS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            bootstrap_servers='localhost:9092'
            )

    for m in consumer:
        print(f"Restarting with new interest {m.value['securities']}")
        symbols = m.value['securities']
        iex.stop()
        time.sleep(1)
        iex = FinStreamer(symbols)
        iex.start()
