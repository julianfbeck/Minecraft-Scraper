from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from pymongo import MongoClient
from pprint import pprint
import os
#connection string based on env 
connection_string = os.environ.get('MONGODB_URL')
if connection_string is None:
    connection_string = "mongodb://root:example@localhost:27017"
kafka_string = os.environ.get('KAFKA_URL')
if kafka_string is None:
    kafka_string = "localhost:9092"
print("kafka string:", kafka_string)
client = MongoClient(connection_string)
db=client.userdata
##create collection

player_collection = client.player_collection
servers_collection = client.servers_collection

consumer = KafkaConsumer("players","server-values",
    bootstrap_servers=[kafka_string],
    api_version=(0, 10, 1),
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    if message.topic == "players":
        print(f"Inserting {message.value['name']}")
        db.player_collection.insert_one(message.value)
    if message.topic == "server-values":
        print(f"Inserting {message.value['ip']}")
        db.servers_collection.insert_one(message.value)