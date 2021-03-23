from kafka import KafkaConsumer
from json import loads
from const import CONST

consumer = KafkaConsumer(
        CONST.TOPIC_TRADES,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers='localhost:9092'
        )

for m in consumer:
    print(m.value)
