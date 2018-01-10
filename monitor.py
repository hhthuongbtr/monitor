import requests
from utils.system_status import SystemStatus
from BLL.agent import Agent

system_status = SystemStatus()
data = {"cpu": system_status.get_cpu(),
        "mem": system_status.get_mem(),
        "disk": system_status.get_disk()
}

agent = Agent()
agent.put(data)

