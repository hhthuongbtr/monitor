import xmlrpclib

class Supervisord:
    def __init__(self):
        self.server = None
        try:
            self.server = self.server = xmlrpclib.Server('http://localhost:9001/RPC2')
        except Exception as e:
            raise e

    def get_server_status(self):
        try:
            return self.server.supervisor.getState()
        except Exception as e:
            return e
    
    def restart_server(self):
        try:
            return self.server.supervisor.restart()
        except Exception as e:
            return e
    def get_process_info(self, name):
        try:
            return self.server.supervisor.getProcessInfo(name)
        except Exception as e:
            return e

    def get_all_process_info(self):
        try:
            return self.server.supervisor.getAllProcessInfo()
        except Exception as e:
            return e

    def start_process(self, name):
        try:
            print self.server.supervisor.startProcess(name)
        except Exception as e:
            return e

    def start_all_processes(self):
        try:
            return self.server.supervisor.startAllProcesses()
        except Exception as e:
            return e

    def start_process_group(self, name):
        try:
            return self.server.supervisor.startProcessGroup(name)
        except Exception as e:
            return e

    def stop_process(self, name):
        try:
            return self.server.supervisor.stopProcess(name)
        except Exception as e:
            return e

    def stop_process_group(self, name):
        try:
            return self.server.supervisor.stopProcessGroup(name)
        except Exception as e:
            return e

    def stop_all_processes(self):
        try:
            return self.server.supervisor.stopAllProcesses()
        except Exception as e:
            return e

    def reload_config(self):
        try:
            return self.server.supervisor.reloadConfig()
        except Exception as e:
            return e

    def add_process_group(self, name):
        try:
            return self.server.supervisor.addProcessGroup(name)
        except Exception as e:
            return e

    def remove_process_group(self, name):
        try:
            return self.server.supervisor.removeProcessGroup(name)
        except Exception as e:
            return e


