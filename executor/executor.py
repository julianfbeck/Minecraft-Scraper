from sys import api_version
from kafka import KafkaConsumer, KafkaAdminClient
from json import dumps, loads
from kafka.admin import NewTopic
import shlex
from subprocess import Popen, PIPE
from threading import Timer
import os
import uuid
import threading
import time
topic = 'servers'
number_of_workers = 5
kafka_string = os.environ.get('KAFKA_URL')
if kafka_string is None:
    kafka_string = "localhost:9092"

print("using kafka:", kafka_string)
def run(cmd, timeout_sec):
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
        ## log stdout and stderr
        if stderr.decode("utf-8") != "":
            print(stderr.decode("utf-8"))
        if stdout.decode("utf-8") != "":
            print(stdout.decode("utf-8"))
    finally:
        timer.cancel()

def setup_partitions():
    consumer = KafkaConsumer(
        topic, bootstrap_servers=kafka_string,  group_id='consumer', auto_offset_reset='latest', api_version=(0, 10, 2), value_deserializer=lambda x: loads(x.decode('utf-8')))
    topics = consumer.topics()
    if not topics: 
        exit(0)
    print("topics:", topics)
    partitions = consumer.partitions_for_topic(topic)
    if not partitions or len(partitions) != number_of_workers:
        print("Creating partitions for number of workers:", number_of_workers)
        # create partitions
        admin_client = KafkaAdminClient(bootstrap_servers=kafka_string, api_version=(0, 10, 2))
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
        bootstrap_servers=kafka_string,
        api_version=(0, 10, 2),
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