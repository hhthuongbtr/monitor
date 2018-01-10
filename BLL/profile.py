from DAL.profile import Profile as ProfileDAL

class Profile:
    def __init__(self):
        self.profile = ProfileDAL()
    def get(self):
        return self.profile.get()
    def put(self, id, data):
        return self.profile.put(id, data)
