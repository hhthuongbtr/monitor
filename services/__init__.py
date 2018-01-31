from os import path, remove
import logging
import logging.config
import json
from config.config import LOGGING as logging_config_dict
 
from .first_check import FirstCheck
from .last_check import LastCheck
from .video_check import VideoCheck
from .monitor import Monitor
from .snmp_agent import Snmp

logging.config.dictConfig(logging_config_dict)
 
# Log that the logger was configured
logger = logging.getLogger(__name__)
logger.info('Completed configuring logger()!')
