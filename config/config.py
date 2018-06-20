SYSTEM = {
    'broadcast_time': {
        'TO': 22, 
        'FROM': 6
        }, 
    'HOST': '10.0.0.205', 
    'libery': {
        'FFPROBE': '/usr/local/bin/ffprobe', 
        'FFMPEG': '/opt/ffmpeg/ffmpeg'
        }, 
    'monitor': {
        'SOURCE': True, 
        'BLACK_SCREEN': False
        }, 
    'BREAK_TIME': 20,
    'RUNNING_BACKUP_QUEUE' : 'running_backup'
    }

API = {
    'master': {
        'URL': '42.117.9.100', 
        'PASSWORD': 'iptv13579', 
        'PORT': 8888, 
        'USER': 'monitor'
        },
    'slave': {
        'ACTIVE': True, 
        'URL': '42.117.9.99', 
        'PASSWORD': 'iptv13579', 
        'PORT': 8888, 
        'USER': 'monitor'
        }
    }

DATABASE = {
    'master': {
        'NAME': 'monitor', 
        'HOST': '118.69.166.134', 
        'USER': 'MonitorAgent', 
        'ACTIVE': True, 
        'PASSWORD': '11nit0rA93nt', 
        'PORT': 3306
        },
    'slave': {
        'NAME': 'monitor', 
        'HOST': '42.144.244.190', 
        'USER': 'MonitorAgent', 
        'ACTIVE': False, 
        'PASSWORD': '11nit0rA93nt', 
        'PORT': 3306
        }
    }

SUPERVISORD={
    'HOST'                  : 'localhost',
    'PORT'                  : 9001,
    'CONF_DIR'              : '/etc/supervisord/conf.d',
    'CONTROL_DIR'           : '/usr/local/bin/supervisorctl',
    'CONF_TEMPLATE_DIR'     : '/monitor/config/supervisord.template',
    'CONF_EXTENSION'        : '.ini'
    }

SOCKET = {
    "HOST"                  :"42.117.9.99",
    "PORT"                  :5672,
    "USER"                  :"monitor",
    "PASSWD"                :"iptv13579"
    }
