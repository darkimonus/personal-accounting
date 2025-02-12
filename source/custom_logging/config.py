LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "main_format": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
            "datefmt": "%H:%M:%S %d-%I-%Y"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "main_format",
        },
        "debug_file": {
            "class": "logging.FileHandler",
            "formatter": "main_format",
            "filename": "debug.log",
        },
        "info_file": {
            "class": "logging.FileHandler",
            "formatter": "main_format",
            "filename": "info.log",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "formatter": "main_format",
            "filename": "error.log",
        },
    },

    "loggers": {
        "debug": {
            "handlers": ["console", "debug_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "info": {
            "handlers": ["console", "info_file"],
            "level": "INFO",
            "propagate": True,
        },
        "error": {
            "handlers": ["console", "error_file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

SYSTEM_DATA_BODY = "> SystemData({0})"

REQUEST_BODY = """REQUEST \nUser: {0}\nSessionId: {1}\nCSRFtoken: {2}\nMethod name: {3}\nRequest path: {4}
Request method: {5}\nStatus code: {6}\nRequest info:\n{7}"""
RESPONSE_BODY = """RESPONSE \nUser - {0}\nSessionId - {1}\nCSRF - {2}\nView - {3}\nTime - ({5})
{4} {6}:Payload ->\n{7}"""
INFO_BODY = """HEADERS: {0},\nOBJECT: {1},\nREFERER: {2},\nQUERY_STRING: {3},\nBODY: {4}\nUSER_IP: {5}
\n-------------------------------------------------\n"""
RESPONSE_INFO_BODY = """HEADERS: {0},\nOBJECT: {1},\nREFERER: {2},\nQUERY_STRING: {3},\nDATA: {4}
\n------------------------------------------------\n"""
