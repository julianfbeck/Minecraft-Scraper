from http import server
import logging
import threading
from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import shlex
from subprocess import Popen, PIPE
from threading import Timer
import concurrent.futures
import os
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

def execute_ping(value):
    consumer = KafkaConsumer(
        'servers',
        bootstrap_servers=[kafka_string],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        client_id="ping-executor"+str(value),
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    for total_requests, message in enumerate(consumer):
        server = message.value.get("server")
        print(f"Request {total_requests} from executor {value} for {server}")
        run(f"python3 ping.py -p {server}", 2)

# number of cores
thread_array = [threading.Thread(target=execute_ping, args=(i,)) for i in range(4)]

for thread in thread_array:
    thread.start()