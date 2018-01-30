from os import path, remove
import logging
import logging.config
import json
 
from .agent import Agent
from .log import Log
from .profile import Profile, Snmp
 
# If applicable, delete the existing log file to generate a fresh log file during each execution
if path.isfile("/var/log/python_logging.log"):
    remove("/var/log/python_logging.log")
 
with open("config/python_logging_configuration.json", 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)
 
logging.config.dictConfig(config_dict)
 
# Log that the logger was configured
logger = logging.getLogger(__name__)
logger.info('Completed configuring logger()!')
