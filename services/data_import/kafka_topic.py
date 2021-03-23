from const import CONST
from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092",
        client_id='test'
        )

topic_list=[]
topic_list.append(NewTopic(name=CONST.TOPIC_SHORT_PUTS, num_partitions=3, replication_factor=2))
admin_client.create_topics(new_topics=topic_list, validate_only=False)
