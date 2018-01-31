from os import path, remove
import logging
import logging.config
import json
from config.config import LOGGING as logging_config_dict
 
from .agent import Agent
from .log import Log
from .profile import Profile, Snmp
 
logging.config.dictConfig(logging_config_dict)
 
# Log that the logger was configured
logger = logging.getLogger(__name__)
logger.info('Completed configuring logger()!')
