import itertools
from time import sleep
from json import dumps
from kafka import KafkaProducer
import random
import masscan
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         api_version=(0, 10, 1),
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
if __name__ == "__main__":
    A = list(range(1, 0xff))
    B = list(range(1, 0xff))
    random.shuffle(A)
    random.shuffle(B)
    ip_ranges = []

    for a, b in itertools.product(A, B):
        ip_range = f"{a}.{b}.0.0/16"
        ip_ranges.append(ip_range)

    while True:
        random.shuffle(ip_ranges)
        for ip_range in ip_ranges:
            print(ip_range)
            try:
                mas = masscan.PortScanner()
                mas.scan(ip_range, ports='25565', arguments='--max-rate 1000')
                print("there are results")
                for ip in mas.scan_result['scan']:
                    host = mas.scan_result['scan'][ip]
                    if "tcp" in host and 25565 in host['tcp']:
                        print(ip)
                        producer.send('servers', value={"server": ip})
                        producer.flush()
            except Exception as e:
                print(e)
        print("Done")
        