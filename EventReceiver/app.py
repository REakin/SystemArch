import connexion
import json

import yaml

from connexion import NoContent
import requests

from pykafka import KafkaClient

import datetime

from flask_cors import CORS, cross_origin

#config
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

#Your functions here

def addRegion(cofRegion):
    client = KafkaClient(hosts=f'{app_config["kafkastore"]["host"]}:{app_config["kafkastore"]["port"]}')
    topic = client.topics['events']
    producer = topic.get_sync_producer() 
    msg = { "type": "region", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),"payload": cofRegion}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201


def addRoast(roastType):
    client = KafkaClient(hosts=f'{app_config["kafkastore"]["host"]}:{app_config["kafkastore"]["port"]}')
    topic = client.topics['events']
    producer = topic.get_sync_producer() 
    msg = { "type": "roast", "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),"payload": roastType}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201


# server setup
app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8070, debug=True)