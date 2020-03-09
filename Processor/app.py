import connexion
import yaml
import os
import logging.config
import logging
from apscheduler.schedulers.background import BackgroundScheduler

import requests
import swagger_ui_bundle
from requests import request
import datetime
import json

from pykafka import KafkaClient
from flask_cors import CORS, cross_origin
from threading import Thread



#config
with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def populate_stats():
    logger.info("Scheduler start")
    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            json_data = json.loads(f.read())
    else:
        json_data = {
            "num_region_stats": 0,
            "num_roast_stats": 0,
            "timeStamp": str(datetime.datetime.now())
        }
    
    parameters = {
        "searchStringstart": json_data['timeStamp'],
        "searchStringend": str(datetime.datetime.now())
    }

    region_data = requests.get(app_config['event_store']['url']+'/region', params=parameters)
    roast_data = requests.get(app_config['event_store']['url']+'/roast', params=parameters)
    
    region_data_json = region_data.json()
    roast_data_json = roast_data.json()

    if region_data.status_code == 200:
        logger.info(f'{len(region_data_json)} new region stats')
    else:
        logger.info('Error: Did not receve 200 code from Region Stats')

    if roast_data.status_code == 200:
        logger.info(f'{len(roast_data_json)} new roast stats')
    else:
        logger.info('Error: Did not receve 200 code from Region Stats')

    if json_data.get('num_region_stats'):
        json_data['num_region_stats'] = len(region_data_json)
    else:
         json_data['num_region_stats'] = json_data['num_region_stats']

    if json_data.get('num_roast_stats'):
        json_data['num_roast_stats'] =  len(roast_data_json)
    else:
         json_data['num_roast_stats'] = json_data['num_roast_stats']

    with open(app_config['datastore']['filename'], "w") as f:
        f.write(json.dumps(json_data))

    logger.debug(f"Total region stats: {json_data['num_region_stats']}. Total roast stats: {json_data['num_roast_stats']}")
    logger.info("Info complete.")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


def get_stats():
    logger.info("Request Received")
    if(os.path.exists(app_config['datastore']['filename'])):
        with open(app_config['datastore']['filename']) as f:
            json_data = json.loads(f.read())

            logger.debug('Request Data:{}'.format(json_data))
            logger.info("Request Complete")
            return json_data, 200
    else:
        logging.debug("Error: file not found")
        return 404

# my fucntion end here :)

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, debug=True)