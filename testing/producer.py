
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaAdminClient
from kafka.admin import NewPartitions

topic = 'kafka'
bootstrap_servers = 'localhost:9092'

# admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
# topic_partitions = {}
# topic_partitions[topic] = NewPartitions(total_count=2)
# admin_client.create_partitions(topic_partitions)
# # admin_client.delete_topics([topic])


producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                        api_version=(0, 10, 2),
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
producer.send("server-values", {'ip': 'John', 'age': 30})

producer.flush()

# for _ in range(100, 20000):
#     msg = {"server": f"{_}"}
#     byte_key = str(_).encode("utf-8")
#     future = producer.send(topic, msg, key=byte_key)
#     print(f'Sending msg: {msg}')
#     result = future.get(timeout=60)


