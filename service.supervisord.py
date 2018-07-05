import os, sys, re
import json
import time
import random
import logging
import logging.config
import logging.handlers
import threading
from utils import SupervisordFile as File
from config import SUPERVISORD, SYSTEM
from rabbit import Rabbit
from BLL import Profile as ProfileBLL
from supervisord import Supervisord

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("sync_alarm")

def create_supervisord_config(ip, name, jid, thomson_host):
    file = File()
    supervisord_config_template = file.read_template()
    base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    supervisord_config = supervisord_config_template.replace('{name}', name)
    supervisord_config = supervisord_config.replace('{ip}', ip)
    supervisord_config = supervisord_config.replace('{jid}', str(jid))
    supervisord_config = supervisord_config.replace('{host}', thomson_host)
    supervisord_config = supervisord_config.replace('{base_dir}', base_dir)
    full_dir =  SUPERVISORD["CONF_DIR"] + '/' + name + SUPERVISORD["CONF_EXTENSION"]
    file.write_conf_file(dir = full_dir, text = supervisord_config)
    logger.info("config file: %s, content: %s"%(full_dir, supervisord_config))
    return 0

def is_ip_multicast(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\{2,5}")
    aa = re.findall(ip_pattern, ip)
    if aa:
        return True
    else:
        return False

def is_ip(ip):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    aa = re.findall(ip_pattern, ip)
    if aa:
        return True
    else:
        return False

def is_json(data):
    try:
        json.loads(data)
        return True
    except:
        return False

def get_ip_from_string(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip = re.findall(ip_pattern, source)
    ip = ip[0]
    return ip

def get_supervisord(name):
    spvs = Supervisord()
    spvs.reload_config()
    spvs.add_process_group(name)
    spvs.start_process(name)
    return 0

def callback(ch, method, properties, body):
    print body
    logger.info("received " + body)
    if not is_ip(body):
        logger.info("received " + body + "not ip.")
        try:
            spvs_code = int(body)
            logger.info("received " + body + "is Supervisord state code")
            if spvs_code == 100:
                logger.info("Supervisord error code = %d --> remove supervisord EXITED job."%(spvs_code))
                spvs = Supervisord()
                t = threading.Thread(target=spvs.remove_exited_job)
                t.start()
            return 0
        except Exception as e:
            logger.warning("Error: received %s detail: %s"%(body, str(e)))
    jid = "None"
    ip = "None"
    thomson_host = "None"
    if is_json(body):
        logger.info("Recieved active backup log: %s"%(str(body)))
        body_data = json.loads(body)
        ip = body_data["source"]
        jid = body_data["jid"]
        thomson_host = body_data["host"]
    else:
        logger.info("Recieved ip source: %s"%(str(body)))
        ip = body
    pf = ProfileBLL()
    data = pf.get_by_ip_multicast(ip)
    if data["status"] == 200:
        profile_list = data["data"]
    else:
        logger.error(str(data["status"]) + " " + data["message"])
        exit(1)
    if not len(profile_list):
        return 0
    name = profile_list[0]['name'] + "_" + profile_list[0]['type'] + "_" + str(jid)
    name = name.replace(" ", "")
    create_supervisord_config(ip, name, jid, thomson_host)
    get_supervisord(name)

def callback2(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print "-------------------------"

if __name__ == "__main__":
    try:
        rb = Rabbit(SYSTEM["HOST"])
        rb.connect()
        rb.channel.basic_consume(callback,
                              queue=rb.routing_key,
                              no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        rb.channel.start_consuming()
    except Exception as e:
        logger.critical(str(e))
        print e
        time.sleep(10)

