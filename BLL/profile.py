from DAL.profile import Profile as ProfileDAL
from DAL.profile import Snmp as SnmpDAL

class Profile:
    def __init__(self):
        self.profile = ProfileDAL()
    def get(self):
        return self.profile.get()
    def put(self, id, data):
        return self.profile.put(id, data)
        
class Snmp:
	def __init__(self):
		self.snmp = SnmpDAL()
	def get(self):
		return self.snmp.get()