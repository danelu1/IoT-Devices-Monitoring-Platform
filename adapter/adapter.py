import os
import logging
import json
import paho.mqtt.client as mqtt
from re import match
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

BROKER = 'mqtt-broker'
PORT = 1883
INFLUXDB_URL = 'http://tsdb:8086'
DEBUG_DATA_FLOW = os.getenv('DEBUG_DATA_FLOW')
DOCKER_INFLUXDB_INIT_ORG = os.getenv('DOCKER_INFLUXDB_INIT_ORG')
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN = os.getenv('DOCKER_INFLUXDB_INIT_ADMIN_TOKEN')
DOCKER_INFLUXDB_INIT_BUCKET = os.getenv('DOCKER_INFLUXDB_INIT_BUCKET')

tsdb_client = InfluxDBClient(
        url=INFLUXDB_URL,
        org=DOCKER_INFLUXDB_INIT_ORG,
        token=DOCKER_INFLUXDB_INIT_ADMIN_TOKEN
    )

def on_message(client, userdata, message):
    if not match(r'[^/]+/[^/]+', message.topic):
        if DEBUG_DATA_FLOW == 'true':
            logging.info(f'Topic {message.topic} does not match the corresponding format!')
        return

    if DEBUG_DATA_FLOW == 'true':
        logging.info(f'Received a message by topic [{message.topic}]')

    location = message.topic.split('/')[0]
    station = message.topic.split('/')[1]
    data = json.loads(message.payload.decode('utf-8'))
    if 'timestamp' not in data:
        timestamp = datetime.now()
        if DEBUG_DATA_FLOW == 'true':
            logging.info('Data timestamp is NOW')
    else:
        timestamp = datetime.fromisoformat(data['timestamp'])
        if DEBUG_DATA_FLOW == 'true':
            logging.info(f'Data timestamp is: {timestamp}')

    for key, value in data.items():
        if type(value) not in [int, float]:
            continue

        if DEBUG_DATA_FLOW == "true" and key != 'timestamp':
            logging.info(f'{location}.{station}.{key} {value}')

        tsdb_client.write_api(write_options=ASYNCHRONOUS).write(
            bucket=DOCKER_INFLUXDB_INIT_BUCKET,
            org=DOCKER_INFLUXDB_INIT_ORG,
            record=Point(f'{location}.{station}')
                    .tag('location', location)
                    .tag('station', station)
                    .field(key, value)
                    .time(timestamp)
        )

    if DEBUG_DATA_FLOW == 'true':
        logging.info('')

if __name__ == '__main__':
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(BROKER, port=PORT)
    client.subscribe("#")
    client.on_message = on_message

    logging.basicConfig(
        level=logging.DEBUG
        if DEBUG_DATA_FLOW == 'true'
        else logging.INFO,
        format='%(asctime)s - %(message)s'
    )

    client.loop_forever()
