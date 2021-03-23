from kafka import KafkaProducer
from json import dumps
from const import CONST

producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers='localhost:9092'
        )

producer.send(
        CONST.TOPIC_LONG_CALLS_PUTS, value={"securities":["BINANCE:BTCUSDT"]}
        )

producer.flush()
