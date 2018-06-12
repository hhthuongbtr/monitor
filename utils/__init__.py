import json
import logging
import logging.config
import logging.handlers

from .file import File, SupervisordFile
from .ffmpeg import Ffmpeg
from .DateTime import DateTime
from .system_status import SystemStatus

with open("/monitor/config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger(__name__)