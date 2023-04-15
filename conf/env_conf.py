import os
import json
import subprocess

import logging
from os import listdir
from os.path import isfile, join


# #Base - Absoulute path:
# BASE_PATH = '//reporting/'
# LOG_PATH = '//reporting/log/'


BASE_PATH = 'C:/Users/mm13854/Desktop/UnitTest_Flask_Dec/cftp_tableau_filecopy/deploy_test/'
LOG_PATH = 'C:/Users/mm13854/Desktop/UnitTest_Flask_Dec/cftp_tableau_filecopy/deploy_test/log/'

# Environment Variable
_ENV = os.environ['RPM_ENVIRONMENT']
_FID = os.environ['USER']
_HOST = os.environ['HOST_NAME']
_PUBLISH_TYPE = os.environ['TABLEAU_PUBLISH_TYPE']
_TABCMD_PATH = os.environ['TABCMD_PATH']
_CYBERARK = os.environ['CYBERARK_TYPE']
_PROJECT_FOLDER = os.environ['PROJECT_FOLDER']
_JOB_TYPE = os.environ['JOB_TYPE']
_JOB_FILE=os.environ['JOB_FILE']
_API_LOG_TYPE=os.environ['RESTAPI_LOG_TYPE']

##Log Configuration
FORMAT = '%(hostname)s %(user)s %(asctime)s : %(message)s'
logging.basicConfig(filename=LOG_PATH+"publishEvent.log",format=FORMAT)
_logConfig = {'hostname': _HOST, 'user': _FID}
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Implement Cyberark only in dev , uat
if _CYBERARK=='DYNAMIC' and _ENV.upper() in ('DEV','SIT','SIT2','SIT3','SIT4','SIT5','SIT6','SIT7','SIT8','UAT','UAT2','UAT3','UAT4','UAT5','UAT6','PROD','PROD1') :
    print("SOFTLINK Version to trigger tabcmd")
    # print(os.system("${_SOFTLINK} version"))
    print('Cyberark is triggered.........')
    TOKEN = json.load(open(BASE_PATH + "secrets/cyberark_env.json"))
    CONFIGURE_TOKEN = json.loads(json.dumps(TOKEN)).get(_ENV)
    KEY = CONFIGURE_TOKEN.get('USER').get('name')
    APPID = CONFIGURE_TOKEN.get('desc').get('appID')
    LDAP_GROUP = CONFIGURE_TOKEN.get('desc').get('Object')
    SAFE = CONFIGURE_TOKEN.get('desc').get('Safe')

    # AppID and ldap group must be declared in sequence 
    # Return value to authenticate | Code will only run after autosys job [ Autosys not implemented ]
    logger.info('Loggin CyberARK : ', extra=_logConfig)
    # Uncomment VALUE when deploying script to server
    # VALUE=subprocess.run(["sh",BASE_PATH + "bin/cyberark.sh",APPID,SAFE,LDAP_GROUP],capture_output=True,text=True).stdout.strip()
    # print(f"autentication success : {VALUE.replace(VALUE,'*******')}")
    # logger.info('Return cyberark : ' + VALUE, extra=_logConfig)
else :
    #Static Implementation    
    print('Cyberark not triggered')
    TOKEN = json.load(open(BASE_PATH + "secrets/auth_fid.json"))
    CONFIGURE_TOKEN = json.loads(json.dumps(TOKEN)).get(_ENV)
    KEY = CONFIGURE_TOKEN.get('USER').get('name')
    VALUE = CONFIGURE_TOKEN.get('TOKEN').get('value')

## ENV URL CONFIGURATION
SERVER_URL = {
    'DEV':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT2':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT3':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT4':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT5':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT6':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT7':{'ENV_URL':'https://dev..tableau.global..net'},
    'SIT8':{'ENV_URL':'https://dev..tableau.global..net'},
    'UAT':{'ENV_URL':'https://uat..tableau.global..net'},
    'UAT2':{'ENV_URL':'https://uat..tableau.global..net'},
    'UAT3':{'ENV_URL':'https://uat..tableau.global..net'},
    'UAT4':{'ENV_URL':'https://uat..tableau.global..net'},
    'UAT5':{'ENV_URL':'https://uat..tableau.global..net'},
    'UAT6':{'ENV_URL':'https://uat..tableau.global..net'},
    'PROD':{'ENV_URL':'https://.tableau.global..net'},
    'PROD1':{'ENV_URL':'https://.tableau.global..net'}
}[_ENV]

# # SITE ID CONFIGURATION
PROJECT_CONFIGURATION = {
    'DEV': {'site': '', 'project': f'{_PROJECT_FOLDER}'},  
    'SIT': {'site': 'SIT', 'project': f'{_PROJECT_FOLDER}'},
    'SIT2': {'site': 'SIT2', 'project': f'{_PROJECT_FOLDER}'},
    'SIT3': {'site': 'SIT3', 'project': f'{_PROJECT_FOLDER}'},
    'SIT4': {'site': 'SIT4', 'project': f'{_PROJECT_FOLDER}'},
    'SIT5': {'site': 'SIT5', 'project': f'{_PROJECT_FOLDER}'},
    'SIT6': {'site': 'SIT6', 'project': f'{_PROJECT_FOLDER}'},
    'SIT7': {'site': 'SIT7', 'project': f'{_PROJECT_FOLDER}'},
    'SIT8': {'site': 'SIT8', 'project': f'{_PROJECT_FOLDER}'},    
    'UAT': {'site': '', 'project': f'{_PROJECT_FOLDER}'},
    'UAT2': {'site': 'UAT2', 'project': f'{_PROJECT_FOLDER}'},
    'UAT3': {'site': 'UAT3', 'project': f'{_PROJECT_FOLDER}'},
    'UAT4': {'site': 'UAT4', 'project': f'{_PROJECT_FOLDER}'},
    'UAT5': {'site': 'UAT5', 'project': f'{_PROJECT_FOLDER}'},
    'UAT6': {'site': 'UAT6', 'project': f'{_PROJECT_FOLDER}'},
    'PROD': {'site': '', 'project': f'{_PROJECT_FOLDER}'},
    'PROD1': {'site': 'PROD1', 'project': f'{_PROJECT_FOLDER}'},
}[_ENV]

FLASK_CONFIGURATION = {
    'DEV':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT2':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT3':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT4':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT5':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT6':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT7':{'ENV_URL':'sd.nam.nsroot.net'},
    'SIT8':{'ENV_URL':'sd.nam.nsroot.net'},
    'UAT':{'ENV_URL':'sd-i77r.nam.nsroot.net'},
    'UAT2':{'ENV_URL':'sd-i77r.nam.nsroot.net'},
    'UAT3':{'ENV_URL':'sd-i77r.nam.nsroot.net'},
    'UAT4':{'ENV_URL':'sd-i77r.nam.nsroot.net'},
    'UAT5':{'ENV_URL':'sd-i77r.nam.nsroot.net'},
    'UAT6':{'ENV_URL':'sd-i77r.nam.nsroot.net'},
    'PROD':{'ENV_URL':'sd-ac3d.nam.nsroot.net'},
    'PROD1':{'ENV_URL':'sd-ac3d.nam.nsroot.net'}
}[_ENV]