#Create Symbolink | Softlink to nas location in home directory 
#Check if FID directories is symbolink exist  
_SOFTLINK=/home/${USER}/tabcmd
if [ -f ${_SOFTLINK} ]
then echo "Tabcmd .2251 Exists, Ignoring condition"
else ln -s /opt/tableau/tableau_server/packages/bin.20212.21.1217.2251/tabcmd ${_SOFTLINK} && echo "Tabcmd .2251 Created"
fi
# Export RPM_ENVIRONMENT is not required as RPM_ENVIRONMENT is declared in jil files as envvars 
export TABLEAU_PUBLISH_TYPE='TABCMD'
export CYBERARK_TYPE='DYNAMIC'
# softlink 
export TABCMD_PATH=${_SOFTLINK}
echo "Tabcmd Version -- "
${_SOFTLINK} version 
export PROJECT_FOLDER='TP Reports'
export JOB_TYPE='workbook_TP'
export JOB_FILE='publish_workbook_TP'
export RESTAPI_LOG_TYPE='TP'

# export hostname 
export HOST_NAME=`echo $(hostname)`

# export TABCMD_PATH=`find /opt/tableau/tableau_server/packages/bin* -type f -name "tabcmd" | sort -t - -V -k 2,2 | head -1`