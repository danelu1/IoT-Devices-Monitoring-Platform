import json
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
from random import choice

BROKER = 'localhost'
PORT = 1883

random_words = ['Non-numerical', 'Values', 'For', 'Testing']

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.connect(BROKER, port=PORT)

while True:
    location = choice(['UPB', 'Dorinel'])
    station = choice(['RPi_1', 'RPi_2', 'RPi_3', 'RPi_4']) if location == 'UPB' else choice(['Zeus', 'Zeu'])

    bat = choice([x for x in range(1, 101)])
    humid = choice([x for x in range(10, 100)])
    temp = choice([10 + 0.1 * i for i in range(int((30 - 10) / 0.1))])

    alarm = choice([x for x in range(0, 11)])
    aqi = choice([x for x in range(5, 31)])
    rssi = choice([x for x in range(1000, 2000)])

    payload = {
        'BAT': bat,
        'HUMID': humid,
        'TMP': temp
    } if location == 'UPB' else {
        'Alarm': alarm,
        'AQI': aqi,
        'RSSI': rssi
    }

    if choice([True, False]):
        timestamp = datetime.now().isoformat()
        payload['timestamp'] = timestamp

    if choice([True, False]):
        payload['non-numerical'] = choice(random_words)

    payload = json.dumps(payload)
    client.publish(f'{location}/{station}', payload)

    print(f'Published {payload} at {location}/{station}')

    sleep(1)
