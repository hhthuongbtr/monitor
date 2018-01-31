SYSTEM = {
    "HOST":"172.28.0.42",
    "monitor": {
        "SOURCE": True,
        "BLACK_SCREEN": True
    },

    "broadcast_time": {
        "FROM": 6,
        "TO": 22
    },

    "libery": {
        "FFPROBE": "/usr/bin/ffprobe",
        "FFMPEG": "/usr/bin/ffmpeg"
    },
    "BREAK_TIME": 15
}

API = {
    "master": {
        "URL": "localhost",
        "PORT": 8888,
        "USER": "monitor",
        "PASSWORD": "iptv13579"
    },

    "slave": {
        "ACTIVE" : False,
        "URL": "localhost",
        "PORT": 8888,
        "USER": "monitor",
        "PASSWORD": "iptv13579"
    }
}

DATABASE = {
    "master": {
        "ACTIVE" : True,
        "HOST": "localhost",
        "NAME": "monitor",
        "USER": "root",
        "PASSWORD": "root",
        "PORT": 3306
    },

    "slave": {
        "ACTIVE" : False,
        "HOST": "localhost",
        "NAME": "monitor",
        "USER": "root",
        "PASSWORD": "root",
        "PORT": 3306
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "/var/log/monior_IPTV.log",
            "encoding": "utf8"
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["file_handler"]
    }
}

