from DAL.agent import Agent as AgentDAL

class Agent:
    def __init__(self):
        self.agent = AgentDAL()
    def put(self, data):
        return self.agent.put(data)
