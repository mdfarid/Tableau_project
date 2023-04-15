import tableauserverclient as TSC
from datetime import datetime
import json
import logging
import warnings
import json
import os
import subprocess

## Import global environment module
import env_conf as conf

## Logging Configuration
FORMAT = '%(hostname)s %(user)s %(asctime)s : %(message)s'
logging.basicConfig(filename="/..../reporting/log/publishEvent.log",format=FORMAT)
_logConfig = {'hostname': conf._HOST, 'user': conf._FID}
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("triggering PublishWorkbook.py......" , extra=_logConfig)
logger.info("Starting publishing Workbook script ...." , extra=_logConfig)


# Log System for UI Integration 
# Log file should be in json format
# Unique_TimeStamp
_timeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
_APILogs = f'/..../reporting/app/logs/publish_{conf._API_LOG_TYPE}_{conf._ENV}_{_timeStamp}.json'

## Read Jobs available to publish workbook 
_workbookJSON = json.load(open(f'/..../reporting/job/{conf._JOB_FILE}.json'))
_workbookDATA = json.loads(json.dumps(_workbookJSON)).get('workbook')

##Publish via server client
##Include Invalid Userbane / Not authorized in list dict for job Failure
def _publishEvent_tableauclient():

    ## -- Load from global current environment
    logger.info("Publishing via tableau server client ",extra=_logConfig)
    server=TSC.Server(conf.SERVER_URL.get('ENV_URL'));
    warnings.filterwarnings("ignore")

    ## -- Global Variable 
    project_id={};
    overwrite_true = TSC.Server.PublishMode.Overwrite

    # -- Login Authentication    
    server.add_http_options({'verify': False})
    tableau_auth = TSC.TableauAuth(conf.KEY, conf.VALUE, conf.PROJECT_CONFIGURATION.get('site'))
    
    logger.info(" *****************************Staring on publish Workbook "+ conf._ENV +"************************************** ", extra=_logConfig)
    logger.info("Deploying to env : " + conf._ENV, extra=_logConfig)
    logger.info("Deploying to site : " + conf.PROJECT_CONFIGURATION.get('site'), extra=_logConfig)
    logger.info("Deploying to server url env : " + conf.SERVER_URL.get('ENV_URL'), extra=_logConfig)


    try:
        server.auth.sign_in(tableau_auth)
        all_project_items, pagination_item = server.projects.get()
        for proj in all_project_items:
            project_id.update({proj.name:proj.id})
        logger.info("Publish Successful ",extra=_logConfig)
    except Exception as e:
        logger.info("Authentication failed, Plese check if password is correct : " + e , extra=_logConfig)

    for counter, workbook in enumerate(_workbookDATA):
        target_project=project_id.get(f"{conf._PROJECT_FOLDER}")
        # target_project=project_id.get(".... Reports")
        try :
            ## Publish Event 
            publish_project_folder = TSC.WorkbookItem(target_project); 
            publish_workbook_job = server.workbooks.publish(publish_project_folder,workbook.get('path'),overwrite_true)
            logger.info("Workbook published. JOB ID: {0}".format(publish_workbook_job.id), extra=_logConfig)
            logger.info("#"+str(counter+1) + " : Workbook Path From : " + workbook.get('path'),extra=_logConfig)
        except Exception as e :
            logger.info("Workbook not published : " + e , extra=_logConfig)

    #Job completed , kill session | End JobList
    server.auth.sign_out()
    logger.info("Job Completed ", extra=_logConfig)
    logger.info("Workbook published to " + conf.SERVER_URL.get('ENV_URL'), extra=_logConfig)
    logger.info("Exiting Application , Publish workbook completed", extra=_logConfig)

##Publish via tabcmd 
def _publishEvent_tabcmd():    
    _JobStatus = [dict() for x in range(0)]
    logger.info(" *****************************Staring on publish Workbook "+ conf._ENV +"************************************** ", extra=_logConfig)
    logger.info("Publishing via tabcmd ",extra=_logConfig)
    logger.info("Environment variable ---> " + conf._PUBLISH_TYPE , extra=_logConfig)   
    logger.info("Deploying to env : " + conf._ENV, extra=_logConfig)
    logger.info("Deploying to site : " + conf.PROJECT_CONFIGURATION.get('site'), extra=_logConfig)
    logger.info("Deploying to server url env : " + conf.SERVER_URL.get('ENV_URL'), extra=_logConfig) 
    for counter, workbook in enumerate(_workbookDATA):

        try :   
            _error_extension=['error','bad request']

            # Get Process Output | Determine if status is succesful or fail
            # --> Get CyberArk Password | Check if it consist of Special Characer Such as (')
            _cyberark = conf.VALUE.find("'")
            _cyberark_result = True if _cyberark > -1 else False        
            print(f"Cyberark consist of (') -> {_cyberark_result}")

            # Special Characters Condition
            # Non Special Characters Condition with $ sign 
            if _cyberark_result :
                _publish = subprocess.getoutput(conf._TABCMD_PATH + " publish '"+workbook.get('path')+"' -o -s "+conf.SERVER_URL.get('ENV_URL')+" -t '"+conf.PROJECT_CONFIGURATION.get('site')+"' -r '"+conf.PROJECT_CONFIGURATION.get('project')+"' --no-certcheck --no-proxy -username "+conf.KEY+" -p " + f'''"{conf.VALUE}"''' + "" )
            else :
                _publish = subprocess.getoutput(conf._TABCMD_PATH + " publish '"+workbook.get('path')+"' -o -s "+conf.SERVER_URL.get('ENV_URL')+" -t '"+conf.PROJECT_CONFIGURATION.get('site')+"' -r '"+conf.PROJECT_CONFIGURATION.get('project')+"' --no-certcheck --no-proxy -username "+conf.KEY+" -p '"+conf.VALUE+"'")
                # _publish = subprocess.getoutput(conf._TABCMD_PATH + " publish '"+workbook.get('path')+"' -o -s "+conf.SERVER_URL.get('ENV_URL')+" -t '"+conf.PROJECT_CONFIGURATION.get('site')+"' -r '"+conf.PROJECT_CONFIGURATION.get('project')+"' --no-certcheck --no-proxy -username "+conf.KEY+" -p " + f'\{conf.VALUE}' + "" )
             
            _publish = _publish.lower()
            print(f"Publish is {_publish}")

            # Raise Exception if job failed | if Fail raise exception error handling to stop job
            # **** Need Adjustment ****
            _error_extension=['error','bad request']

            _status = [ele for ele in _error_extension if(ele in _publish)]
            _PublishStatus = "Failure" if bool(_status) else "Success"

            # if _PublishStatus != "Sucessful" : #Kill Loop
            #     raise Exception("Published Failed")

            # if _publish != "Sucessful" : #Kill Loop :
            #     _JobStatus.append({"Workbook_name":workbook.get('filename') , "Workbook_status":"Failure", "Workbook_path":workbook.get('path') , "Remarks":e})
            #     raise Exception(f"Publish failed on : {workbook.get('filename')}")
            # os.system(conf._TABCMD_PATH + " publish '"+workbook.get('path')+"' -o -s "+conf.SERVER_URL.get('ENV_URL')+" -t '"+conf.PROJECT_CONFIGURATION.get('site')+"' -r '"+conf.PROJECT_CONFIGURATION.get('project')+"' --no-certcheck --no-proxy -username "+conf.KEY+" -p '"+conf.VALUE+"'")        
            _JobStatus.append({"FileName":_APILogs.rsplit('/', 1)[1],"Workbook_name":workbook.get('filename') , "Workbook_status":_PublishStatus , "Workbook_path":workbook.get('path') , "Remarks":_publish})
            logger.info("Publish Succesful for : " + workbook.get('filename')  ,extra=_logConfig)
            logger.info("Publish Succesful to env : " + conf.PROJECT_CONFIGURATION.get('site')  ,extra=_logConfig)
            logger.info("Publish Succesful to project : " + conf.PROJECT_CONFIGURATION.get('project')  ,extra=_logConfig)
            logger.info("#"+str(counter+1) + " : Workbook Path From :  " + workbook.get('path'),extra=_logConfig)
            print(f'success, {workbook} deployed')
        except Exception as e :
            logger.info('Workbook not publish , check log ' + e , extra._logConfig)
            _JobStatus.append({"Workbook_name":workbook.get('filename') , "Workbook_status":"Failure", "Workbook_path":workbook.get('path') , "Remarks":e})
            print('Fail Trigger : ')
            print(e)        
    logger.info(" Job Files Created ", extra=_logConfig)

    _JobString = json.dumps(_JobStatus, indent=4, sort_keys=True)
    _JobSaved = open(_APILogs, "w")
    _JobSaved.write(_JobString)
    _JobSaved.close()

    os.system(f"chmod -R 777 {_APILogs}")
    logger.info(" *****************************Ending on publish Workbook "+ conf._ENV +"************************************** ", extra=_logConfig)

###Determining publish method via publish type declared in postInstall Script
def _runMain():
    if conf._PUBLISH_TYPE == 'TABCMD' :
        _publishEvent_tabcmd()
    else :
        _publishEvent_tableauclient()

# #-- Trigger publish component
_runMain()