import connexion
import yaml

from connexion import NoContent
from requests import request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import mysql.connector

import json

from base import Base
from Region import Region
from Roast import Roast

import datetime

from threading import Thread
from pykafka import KafkaClient

import logging
import logging.config

from flask_cors import CORS, cross_origin


#config
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


#db setup
DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@localhost:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

#Your functions here
# def addRegion(cofRegion):
#     session = DB_SESSION()
#     region = Region(cofRegion['id'],
#                     cofRegion['name'])
#     session.add(region)
#     session.commit()
#     session.close()
#     return NoContent, 201

def getRegion(searchStringstart, searchStringend):
    results_list = []

    session = DB_SESSION()

    results = []

    results = session.query(Region).filter(Region.date_created >= searchStringstart, Region.date_created <= searchStringend)

    for result in results:
        results_list.append(result.to_dict())
    session.close()

    return results_list, 200

# def addRoast(roastType):
#     print(roastType)
#     session = DB_SESSION()
#     roast = Roast(
#                   roastType['id'],
#                   roastType['name'],
#                   roastType['region'])
#     session.add(roast)
#     session.commit()
#     session.close()
#     return NoContent, 201


def getRoast(searchStringstart, searchStringend):
    results_list = []

    session = DB_SESSION()

    results = []

    results = session.query(Roast).filter(Roast.date_created >= searchStringstart, Roast.date_created <= searchStringend)


    for result in results:
        results_list.append(result.to_dict())
    session.close()

    return results_list, 200

def process_messages():
    client = KafkaClient(hosts=f"{app_config['kafkastore']['host']}:{app_config['kafkastore']['port']}")
    topic = client.topics[f"{app_config['topic']}"]
    consumer = topic.get_simple_consumer(consumer_group="events", auto_commit_enable=True, auto_commit_interval_ms=1000)

    for message in consumer:
        message_string = message.value.decode('utf-8')
        message = json.loads(message_string)
        logger.info(f'New Message: {message_string}')
        if message['type'] == 'region':
            session=DB_SESSION()
            region = Region(message['payload']['id'],
                          message['payload']['name'])

            session.add(region)
            session.commit()
            session.close()

        if message['type'] == 'roast':
            session=DB_SESSION()
            roast = Roast(message['payload']['id'],
                            message['payload']['name'],
                            message['payload']['region'])
            session.add(roast)
            session.commit()
            session.close()




#my functions end here 

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)