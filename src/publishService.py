#!/bin/python3

import json
import os
import logging
from os import listdir
from os.path import isfile, join

## Import global environment module
import env_conf as conf

## Global Directory - Absolute path 
# WORKBOOK_PATH = os.popen(f"echo $(ls -td /..../reporting/{conf._JOB_TYPE}/* | sort -t'-' -nk2.3 | tail -1)").read().split('\n')[0] + '/'
WORKBOOK_PATH=f"/..../reporting/{conf._JOB_TYPE}/"
BASE_PATH = '/..../reporting/'
LOG_PATH = '/..../reporting/log/'

##Log Configuration
FORMAT = '%(hostname)s %(user)s %(asctime)s : %(message)s'
logging.basicConfig(filename=LOG_PATH+"publishEvent.log",format=FORMAT)
_logConfig = {'hostname': conf._HOST, 'user': conf._FID}
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("publishService.py triggered......" , extra=_logConfig)
logger.info("Starting publishing Service script ...." , extra=_logConfig)

# logger.info('Staring PublishServie to create JOB Json File' , extra=_logConfig)
def createJson():
    logger.info(" *****************************Staring on publish Service "+ conf._ENV +"************************************** ", extra=_logConfig)

    ## Store all filename as array
    _Files = [file for file in listdir(WORKBOOK_PATH) if isfile(join(WORKBOOK_PATH, file))]
    _json ='{"workbook":['

    ## Write Json Format
    for filename in _Files:
        _json += '{"filename":"'+ filename +'","path":"'+WORKBOOK_PATH+filename+'"}'
        if filename != _Files[-1]:
            _json += ','
    _json += '],"publish":{"method":"overwrite","type":"workbook"}}'
    logger.info('Total of JOBS created : ' + ' '+  str(len(_Files)) , extra=_logConfig)

    ## Dump as Json format
    event_dict = json.loads(_json)
    _jsonFile = json.dumps(event_dict, indent = 4, sort_keys=True)
    logger.info('Jobs Created ' , extra=_logConfig)

    ## Save Json File
    base = '/..../reporting/job/'
    _saveFile = base + f'{conf._JOB_FILE}.json'
    with open(_saveFile, 'w') as f:
        for line in _jsonFile:
            f.write(line)
    logger.info("Saving json file on : " + str(_saveFile), extra=_logConfig)

    ## Create Permission to Job Folder
    # os.system("chmod -R 777 "+BASE_PATH+"job")
    #os.system(f'chmod -R 777 {BASE_PATH}job/{conf._JOB_FILE}.json')
    logger.info(" *****************************Ending on publish Service "+ conf._ENV +"************************************** ", extra=_logConfig)
    
## Run python Application
createJson()