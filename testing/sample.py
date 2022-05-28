from json import dumps
import re
from subprocess import Popen, PIPE
import uuid
import os
from kafka import KafkaProducer
kafka_string = os.environ.get('KAFKA_URL')
if kafka_string is None:
    kafka_string = "localhost:9092"



def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line
    process.kill()



if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=[kafka_string],
                        api_version=(0, 10, 2),
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))

    for path in run("sudo masscan -p25565 0.0.0.0/0 --max-rate 100 --exclude 255.255.255.255"):
        output = path.decode("utf-8")
        ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', output)
        for ip in ips:
            print("Found ip:", ip)
            producer.send('servers', key=str.encode(str(uuid.uuid4())) ,value={"server": ip})
            producer.flush()