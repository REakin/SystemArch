import connexion
from connexion import NoContent
import requests
import datetime
import json
import yaml
from pykafka import KafkaClient
import logging
import logging.config

from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

#Your functions here
def get_offset_region(offset):
    client = KafkaClient(hosts=f"{app_config['kafka']['server']}:{app_config['kafka']['port']}")
    topic = client.topics["events"]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        logger.info('New Message:',)
        message = json.loads(message_string)
        if message['type'] == 'region':
            message_list.append(message)
    try:
        return message_list[offset], 200
    except:
        return NoContent, 404

def get_oldest_roast():
    client = KafkaClient(hosts=f"{app_config['kafka']['server']}:{app_config['kafka']['port']}")
    topic = client.topics["events"]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        #print(message_string)
        message = json.loads(message_string)
        if message['type'] == 'roast':
            message_list.append(message)
        if len(message_list) == 0:
            return NoContent, 404

        return message_list[-1], 200

# server setup

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8120)