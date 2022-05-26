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

client = MongoClient(connection_string)
db=client.userdata
##create collection
sample_server = {'ip': 'play.pokesaga.org', 'text': '', 'version': 'Velocity 1.7.2-1.18', 'online': 266, 'players': [{'name': '§b       §k§liii§r  §e§lPokeSaga Pixelmon  §r§b§l§kiii', 'uuid': '00000000-0000-0000-0000-000000000000', 'server': 'play.pokesaga.org'}, {'name': '§e              §6§l> REFORGED 8.4.2 <', 'uuid': '00000000-0000-0000-0000-000000000000', 'server': 'play.pokesaga.org'}, {'name': '', 'uuid': '00000000-0000-0000-0000-000000000000', 'server': 'play.pokesaga.org'}, {'name': '§a§lWEBSITE  §fpokesaga.org', 'uuid': '00000000-0000-0000-0000-000000000000', 'server': 'play.pokesaga.org'}, {'name': '§b§lVOTE     §fpokesaga.org/vote', 'uuid': '00000000-0000-0000-0000-000000000000', 'server': 'play.pokesaga.org'}, {'name': '§c§lSHOP     §fbuy.pokesaga.org', 'uuid': '00000000-0000-0000-0000-000000000000', 'server': 'play.pokesaga.org'}], 'status': {'version': {'protocol': 757, 'name': 'Velocity 1.7.2-1.18'}, 'players': {'online': 266, 'max': 2000, 'sample': [{'name': '§b       §k§liii§r  §e§lPokeSaga Pixelmon  §r§b§l§kiii', 'id': '00000000-0000-0000-0000-000000000000'}, {'name': '§e              §6§l> REFORGED 8.4.2 <', 'id': '00000000-0000-0000-0000-000000000000'}, {'name': '', 'id': '00000000-0000-0000-0000-000000000000'}, {'name': '§a§lWEBSITE  §fpokesaga.org', 'id': '00000000-0000-0000-0000-000000000000'}, {'name': '§b§lVOTE     §fpokesaga.org/vote', 'id': '00000000-0000-0000-0000-000000000000'}, {'name': '§c§lSHOP     §fbuy.pokesaga.org', 'id': '00000000-0000-0000-0000-000000000000'}]}, 'description': {'extra': [{'color': 'aqua', 'extra': [{'strikethrough': True, 'text': '----'}], 'text': '   '}, {'strikethrough': True, 'color': 'gold', 'text': '-----'}, {'strikethrough': True, 'color': 'yellow', 'text': '-----'}, {'color': 'white', 'text': '['}, {'text': ' '}, {'bold': True, 'color': 'aqua', 'text': 'Poke'}, {'bold': True, 'color': 'gold', 'text': 'Saga'}, {'text': ' '}, {'color': 'white', 'text': ']'}, {'strikethrough': True, 'color': 'yellow', 'text': '-----'}, {'strikethrough': True, 'color': 'gold', 'text': '-----'}, {'strikethrough': True, 'color': 'aqua', 'text': '----\n'}, {'bold': True, 'obfuscated': True, 'color': 'white', 'text': ':'}, {'text': ' '}, {'underlined': True, 'color': 'aqua', 'text': 'Guilds & Quests'}, {'text': ' '}, {'color': 'dark_gray', 'text': '« '}, {'bold': True, 'color': 'yellow', 'text': 'WORLD BOSSES'}, {'text': ' '}, {'color': 'dark_gray', 'text': '» '}, {'underlined': True, 'color': 'aqua', 'text': 'Custom /Skills'}, {'text': ' '}, {'bold': True, 'obfuscated': True, 'color': 'white', 'text': ':'}], 'text': ''}, 'favicon': '', 'modinfo': {'type': 'FML', 'modList': []}}}

player_collection = client.player_collection
servers_collection = client.servers_collection

consumer = KafkaConsumer("players","server-values",
    bootstrap_servers=[kafka_string],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    if message.topic == "players":
        print(f"Inserting {message.value['name']}")
        db.player_collection.insert_one(message.value)
    if message.topic == "server-values":
        print(f"Inserting {message.value['ip']}")
        db.servers_collection.insert_one(message.value)