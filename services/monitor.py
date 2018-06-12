import logging
import requests
from utils.system_status import SystemStatus
from BLL.agent import Agent

class Monitor(object):
    """docstring for Monitor"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def monitor(self):       
        system_status = SystemStatus()
        data = {"cpu": system_status.get_cpu(),
                "mem": system_status.get_mem(),
                "disk": system_status.get_disk()
        }
        self.logger.info(str(data))
        agent = Agent()
        agent.put(data)

