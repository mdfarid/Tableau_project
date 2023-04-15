#!/bin/bash


#Configurable Publish Type
#Option : 'TABLEAUCLIENT' or 'TABCMD'
#Export variable for python script to use 
#Find path dynamically as it will change after new patches
#Option CYBERARK_TYPE : STATIC OR DYNAMIC
export TABLEAU_PUBLISH_TYPE='TABCMD'
export CYBERARK_TYPE='STATIC'
export TABCMD_PATH=`find /opt/tableau/tableau_server -type f -name "tabcmd"`
# export TABCMD_PATH="$(ls -rt -1 /opt/tableau/tableau_server/packages/bin*/tabcmd| head -1 | xargs -i{} dirname {})"  

# Global Variables 
RLM_BASE_FOLDER=/tmp
TABLEAU_EXTENSION_FOLDER=/opt/tableau/tableau_data/data/tabsvc/httpd/htdocs
TABLEAU_REPORTING_FOLDER=/..../reporting/workbook_TP
TABLEAU_BASE_FOLDER=/..../reporting

# Global for flask variables
TABLEAU_FLASK_FOLDER=/..../reporting/app


echo "Environment hostname : " ${HOSTNAME}
echo "RLM Environment : " ${RPM_ENVIRONMENT}
echo "whoami $(whoami)"

_logger() {
    message=$1
    DATE=`date '+%m-%d-%Y'`
    echo "$HOSTNAME $DATE : $message" | tee -a ${TABLEAU_BASE_FOLDER}/log/postInstall.log
}

# Logging Environment 
_logger "Environment ${RPM_ENVIRONMENT}"
_logger "user $USER or ${USER}"

## Activiate virtual environment Python 3 for PublishEvent 
PYTHON3_OR_ABOVE=/opt/rh/rh-python38/root/usr/bin/python  && _logger "${PYTHON3_OR_ABOVE}"
RLM_ENV=${RPM_ENVIRONMENT} && _logger "${RLM_ENV}"
TBFW_BASE_PATH=/..../${RLM_ENV,,}/app/cftp_tableau_framework && _logger "${TBFW_BASE_PATH}"
_logger "Activating python virtual env"
source ${TBFW_BASE_PATH}/.tbfw_python3/bin/activate  
export PYTHON3_OR_ABOVE=${TBFW_BASE_PATH}/.tbfw_python3/bin/python 

## Environment Variable Setup
## DEV Environment
DEVFRAMEWORK="https://dev......tableau.global..net/...._Export.html";
DEVENVIRONMENT="https://dev......tableau.global..net";

## UAT Enviroment 
UATFRAMEWORK="https://uat......tableau.global..net/...._Export.html";
UATENVIRONMENT="https://uat......tableau.global..net";

## PROD Environment 
PRODFRAMEWORK="https://Prod.....tableau.global..net/...._Export.html";
PRODENVIRONMENT="https://Prod.....tableau.global..net";


#-> First Parameter is Target Folder 
#-> Second Parameter is Message
#-> File & Directory is 2 different things -d & -f
_createFolder(){
    if [ -d $1 ]
    then echo "$2 Directory Already Exists"
    else mkdir $1 && chmod -R 777 $1 && echo "$2 Directory Created & Permission set executable for all"
    fi
}

# If File Exist 
_createFolder_File(){
    if [ -f $1 ]
    then echo "$2 Directory Already Exists"
    else touch $1 && chmod -R 777 $1 && echo "$2 Directory Created & Permission set executable for all"
    fi
}

# Create Job Directory
_createDirectory(){
    # then _logger "Reporting Directory Already Exists" && rm -r ${TABLEAU_BASE_FOLDER} && mkdir ${TABLEAU_BASE_FOLDER} && _logger "Reporting Directory Created"


    _logger "Creating Directory for ${TABLEAU_BASE_FOLDER}"
    # - Main Directory -
    _createFolder ${TABLEAU_BASE_FOLDER} "Reporting Directory"
    _createFolder ${TABLEAU_BASE_FOLDER}/job "Job"
    _createFolder ${TABLEAU_BASE_FOLDER}/src "Src"
    _createFolder ${TABLEAU_BASE_FOLDER}/log "logs"
    _createFolder ${TABLEAU_BASE_FOLDER}/secrets "Secrets"
    _createFolder ${TABLEAU_BASE_FOLDER}/workbook_TP "Workbook TP"
    _createFolder ${TABLEAU_BASE_FOLDER}/bin "Bin"
    _createFolder ${TABLEAU_BASE_FOLDER}/temp "Temp"
    _createFolder ${TABLEAU_BASE_FOLDER}/test_cases "test_cases"

    # -> Update Script to -f
    _createFolder_File ${TABLEAU_BASE_FOLDER}/log/publishEvent.log "Publish log"
    _createFolder_File ${TABLEAU_BASE_FOLDER}/job/publish_workbook_TP.json "TP Workbook"
    _createFolder_File ${TABLEAU_BASE_FOLDER}/job/publish_workbook_LP.json "LP Workbook"
    _createFolder_File ${TABLEAU_BASE_FOLDER}/log/subscription.log "subscription log" 

    _logger "Creating Directory for ${TABLEAU_FLASK_FOLDER}"
    
    # - Create RestAPI Flask Directory -
    cp -R ${RLM_BASE_FOLDER}/app  ${TABLEAU_BASE_FOLDER}
    


    #**************** Move python files for flask ******************
    _logger "Copying publish component to ${TABLEAU_FLASK_FOLDER}"


    #**************** Move python script from tmp to src folder ******************
    _logger "Copying publish component to ${TABLEAU_BASE_FOLDER}/src/"
    cp ${RLM_BASE_FOLDER}/src/publishService.py ${TABLEAU_BASE_FOLDER}/src && _logger "Copied PublishService.py to ${TABLEAU_BASE_FOLDER}/src"
    cp ${RLM_BASE_FOLDER}/src/publishWorkbook.py ${TABLEAU_BASE_FOLDER}/src  && _logger "Copied Publishworkbook.py to ${TABLEAU_BASE_FOLDER}/src"
    cp ${RLM_BASE_FOLDER}/src/env_conf.py ${TABLEAU_BASE_FOLDER}/src  && _logger "Copied env_conf.py to ${TABLEAU_BASE_FOLDER}/src"
    cp ${RLM_BASE_FOLDER}/secrets/auth_fid.json ${TABLEAU_BASE_FOLDER}/secrets  && _logger "Copied auth_fid.json to ${TABLEAU_BASE_FOLDER}/secrets"
    cp ${RLM_BASE_FOLDER}/secrets/cyberark_env.json ${TABLEAU_BASE_FOLDER}/secrets  && _logger "Copied cyberark_env.json to ${TABLEAU_BASE_FOLDER}/secrets"
    cp ${RLM_BASE_FOLDER}/bin/cyberark.sh ${TABLEAU_BASE_FOLDER}/bin  && _logger "Copied cyberark.sh to ${TABLEAU_BASE_FOLDER}/bin"   
    cp ${RLM_BASE_FOLDER}/bin/publish_service.sh ${TABLEAU_BASE_FOLDER}/bin  && _logger "Copied publish.sh to ${TABLEAU_BASE_FOLDER}/bin"
    cp ${RLM_BASE_FOLDER}/bin/publish_LP_env.profile ${TABLEAU_BASE_FOLDER}/bin  && _logger "Copied LP profile file to ${TABLEAU_BASE_FOLDER}/bin"
    cp ${RLM_BASE_FOLDER}/bin/publish_TP_env.profile ${TABLEAU_BASE_FOLDER}/bin  && _logger "Copied TP profile file to ${TABLEAU_BASE_FOLDER}/bin"
    cp ${RLM_BASE_FOLDER}/bin/flask_conf.sh ${TABLEAU_BASE_FOLDER}/bin  && _logger "Copied flask Conf file to ${TABLEAU_BASE_FOLDER}/bin"
    
    
    # ***************** Subscribe functionality Files ****************************
    # Secrets -> Give Absolute path for
    _logger "Copying Subscription Files to ${TABLEAU_BASE_FOLDER}/***"
    cp ${RLM_BASE_FOLDER}/src/excel_conf.py ${TABLEAU_BASE_FOLDER}/src  && _logger "Copied excel configuration file to ${TABLEAU_BASE_FOLDER}/src"
    cp ${RLM_BASE_FOLDER}/src/subscription.py ${TABLEAU_BASE_FOLDER}/src  && _logger "Copied subscription file to ${TABLEAU_BASE_FOLDER}/src"
    cp ${RLM_BASE_FOLDER}/bin/subscription.sh ${TABLEAU_BASE_FOLDER}/bin  && _logger "Copied subscription autosys shell file to ${TABLEAU_BASE_FOLDER}/bin"
    cp ${RLM_BASE_FOLDER}/temp/subscription_scheduler.json ${TABLEAU_BASE_FOLDER}/job  && _logger "Copied Subscription Jobs to ${TABLEAU_BASE_FOLDER}/job"

    # ***************** Test Cases Files ****************************
    logger "Copying Test Cases Files"
    cp ${RLM_BASE_FOLDER}/test_cases/test_tbrp_case.py ${TABLEAU_BASE_FOLDER}/test_cases  && _logger "Copied test_tbrp_case test case file to ${TABLEAU_BASE_FOLDER}/test_case"


    _logger "Adding executable permission "
    chmod -R 777 ${TABLEAU_BASE_FOLDER}
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/app
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/bin
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/job
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/src
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/log
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/temp
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/secrets
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/log/publishEvent.log
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/bin/subscription.sh
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/job/subscription_scheduler.json
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/job/publish_workbook_TP.json
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/job/publish_workbook_LP.json
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/log/subscription.log

    # -> Chmod for Flask Application  
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/app/temp/TBRP_Status.log
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/app/temp/run_flask.out
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/app/temp/run_flask.err
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/app/temp/TBRP_Process.pid

    # -> Chmod for test case Files
    chmod -R 777 ${TABLEAU_BASE_FOLDER}/test_cases/test_tbrp_case.py

}

# Move Extension File Copies [ Excel Extension ]
_extensionFiles(){
    cp ${RLM_BASE_FOLDER}/script/* ${TABLEAU_EXTENSION_FOLDER}/
    chmod -R 777 ${TABLEAU_EXTENSION_FOLDER}
    ls -ltr ${TABLEAU_EXTENSION_FOLDER}/
    _logger "ENV --> ${RPM_ENVIRONMENT}"
    _logger "cs folReporting Extension has been succesfully deployed to ${RPM_ENVIRONMENT} htdoder"
    Copying_File_names=`ls ${RLM_BASE_FOLDER}/script/* ${TABLEAU_EXTENSION_FOLDER}/`
    _logger "$Copying_File_names" && _logger "Files were moved to htdocs folder"
    
}

# Update Twb XML Content
_updateXMLContent(){

    cp ${RLM_BASE_FOLDER}/workbook_TP/*.twbx ${TABLEAU_REPORTING_FOLDER}
    
    #Latest Folder Variable 
    TABLEAU_UPDATE_FOLDER=${TABLEAU_REPORTING_FOLDER}
    chmod -R 777 ${TABLEAU_UPDATE_FOLDER}
    _logger "Workbook reporting Folder Copied : ${TABLEAU_UPDATE_FOLDER}" 

    # convert twbx extension to zip extension
    for file in ${TABLEAU_UPDATE_FOLDER}/*.twbx
    do mv "$file" "${file%.twbx}.z"; done
    _logger  "Files were converted to Z extension"

    ## Unzip all files and replace image folder if found
    unzip -o "${TABLEAU_UPDATE_FOLDER}/*.z" -d ${TABLEAU_UPDATE_FOLDER} 
    _logger "Unzippping all the files and Image Replaced(if existes)"

    # update XML content based on environment
    for file in ${TABLEAU_UPDATE_FOLDER}/*.twb
    do 
      sed -i "s,$1,$2,g" "$file"
      sed -i "s,website='$3',website='$4',g" "$file" 
    done
    _logger "Updating XML Extension environment content from : $1 to $2"
    _logger "Updating XML Server   environment content from : $3 to $4" 

    ##compress files with its subfolders
    cd ${TABLEAU_UPDATE_FOLDER} && for file in *.twb; do zip -r "${file::-4}".zip "$file" Image ; done
    _logger "Files compressing with its subfolder were succeeded"

    ## Remove [twb file], [Image] , [.z] files
    Removing_File_names=`ls ${TABLEAU_UPDATE_FOLDER}/`
    _logger "Removing files from ${TABLEAU_UPDATE_FOLDER}" && _logger "$Removing_File_names"
    rm ${TABLEAU_UPDATE_FOLDER=}/*.twb; rm -r ${TABLEAU_UPDATE_FOLDER}/Image; rm ${TABLEAU_UPDATE_FOLDER}/*.z
    _logger "Image,twb and z files were removed from ${TABLEAU_UPDATE_FOLDER}"

    ## convert .z extension to twbx extension file
    for file in ${TABLEAU_UPDATE_FOLDER=}/*.zip; do mv "$file" "${file%.zip}.twbx"; done
    _logger ".z Extensions files were converted to twbx extension files"
    
    _logger "Show Workbook Directory List : $(ls ${TABLEAU_UPDATE_FOLDER})"
    _logger "XML Content Updated...."
    _logger "ENV --> ${RPM_ENVIRONMENT}"

}

if [[ "$RPM_ENVIRONMENT" == @(DEV|SIT|SIT2|SIT3|SIT4) ]] 
then   
    _logger "Create required directory"
    _createDirectory
        
    _logger "Deploying Extension Folder to ${RPM_ENVIRONMENT}"
    _extensionFiles

    _logger "Deploying Workbook to .... Workbook"
    _updateXMLContent $DEVFRAMEWORK $DEVFRAMEWORK $DEVENVIRONMENT $DEVENVIRONMENT

    _logger "Publish component will be triggered as part of autosys job"
elif [[ "$RPM_ENVIRONMENT" == @(UAT|UAT2|UAT3|UAT4|UAT5|UAT6) ]]
then 

    _logger "Create required directory"
    _createDirectory

    _logger "Deploying Extension Folder to ${RPM_ENVIRONMENT}"
    _extensionFiles

    _logger "Deploying Workbook to .... Workbook"
    _updateXMLContent $DEVFRAMEWORK $UATFRAMEWORK $DEVENVIRONMENT $UATENVIRONMENT

    _logger "Publish component will be triggered as part of autosys job"
elif [[ "$RPM_ENVIRONMENT" == @(PROD|PROD1) ]]
then

    _logger "Create required directory"
    _createDirectory

    _logger "Deploying Extension Folder to ${RPM_ENVIRONMENT}"
    _extensionFiles

    _logger "Deploying Workbook to .... Workbook"
    _updateXMLContent $DEVFRAMEWORK $PRODFRAMEWORK $DEVENVIRONMENT $PRODENVIRONMENT

    _logger "Publish component will be triggered as part of autosys job"
fi
#End of postinstall.sh