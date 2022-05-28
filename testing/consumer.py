from json import loads
import time
from kafka import KafkaAdminClient, KafkaConsumer
from kafka.structs import TopicPartition 
from kafka.admin import NewPartitions, NewTopic
from threading import Timer
import os
import uuid
import threading
topic = 'kafka'
bootstrap_servers = 'localhost:9092'

number_of_workers = 300
def setup_partitions():
    consumer = KafkaConsumer(
        topic, bootstrap_servers=bootstrap_servers,  group_id='consumer', auto_offset_reset='latest', value_deserializer=lambda x: loads(x.decode('utf-8')))

    partitions = consumer.partitions_for_topic(topic)
    if not partitions or len(partitions) != number_of_workers:
        print("Creating partitions for number of workers:", number_of_workers)
        # create partitions
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, api_version=(0, 10, 2))
        topics = consumer.topics()
        ## check if topic exists
        if topic in topics:
            res =  admin_client.delete_topics([topic])
            time.sleep(1)
        admin_client.create_topics([NewTopic(topic, number_of_workers, 1)])
        time.sleep(1)

def execute_ping(value):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[bootstrap_servers],
        client_id=str(uuid.uuid4()),
        group_id='my-group',
        auto_offset_reset='latest',
        enable_auto_commit=True,
        auto_commit_interval_ms =  5000,
        max_poll_records = 100,
        
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    partitions = consumer.partitions_for_topic(topic)
    print(f"Executor created: {value} for {len(partitions)} partitions")
    for total_requests, message in enumerate(consumer):
        server = message.value.get("server")
        print(f"Request {total_requests} from executor {value} for {server}")
        run(f"python3 ping.py -p {server}", 2)

setup_partitions()
thread_array = [threading.Thread(target=execute_ping, args=(i,)) for i in range(number_of_workers)]

for thread in thread_array:
    thread.start()