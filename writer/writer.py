from kafka import  KafkaConsumer
from json import  loads
from pymongo import MongoClient
import os
import uuid
#connection string based on env 
connection_string = os.environ.get('MONGODB_URL')
if connection_string is None:
    connection_string = "mongodb://root:example@localhost:27017"
print("mongodb connection string:", connection_string)
kafka_string = os.environ.get('KAFKA_URL')
if kafka_string is None:
    kafka_string = "localhost:9092"
print("kafka string:", kafka_string)
client = MongoClient(connection_string)

# create database
db=client.userdata
# create collection
player_collection = client.player_collection
servers_collection = client.servers_collection

consumer = KafkaConsumer("players","server-values",
    bootstrap_servers=[kafka_string],
    api_version=(0, 10, 2),
    client_id=str(uuid.uuid4()),
    group_id='my-group',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    auto_commit_interval_ms =  5000,
    max_poll_records = 100,
    value_deserializer=lambda x: loads(x.decode('utf-8')))
print("consumer created")
topics = consumer.topics()

if not topics: 
    exit(0)
print("topics:", topics)


for message in consumer:
    if message.topic == "players":
        print(f"Inserting {message.value['name']}")
        db.player_collection.insert_one(message.value)
    if message.topic == "server-values":
        print(f"Inserting {message.value['ip']}")
        db.servers_collection.update_one({"ip": message.value['ip']}, {"$set":message.value}, upsert=True)