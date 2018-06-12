import json
import logging
import logging.config
import logging.handlers

from .first_check import FirstCheck
from .last_check import LastCheck
from .video_check import VideoCheck
from .as_required_check import AsRequiredCheck
from .monitor import Monitor
from .snmp_agent import Snmp, AgentSnmp

with open("/monitor/config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger(__name__)

