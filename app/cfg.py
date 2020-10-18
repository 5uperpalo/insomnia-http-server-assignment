import logging

tron_url = "https://api.trongrid.io/v1/accounts/"

API_key = "test_key"

test_wallet_address = "TU7Qu3vRSufcetba8qa4CrJuqRY2Sc7TCQ"

client_input_schema = {
    "type": "object",
    "properties": {
        "address": {"type": "string"},
        },
    "required": ["address"]
    }

server_response_schema = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "meta": {"type": "object"},
        "data": {"type": "array"},
        },
    "required": ["success", "meta", "data"]
    }

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "f": {
            "format": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"}
        },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "f",
            "level": logging.INFO
            },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/main.log",
            "mode": "a",
            "maxBytes": 100000,
            "backupCount": 5,
            "formatter": "f",
            "level": logging.INFO
            },
        },
    "loggers": {
        "": {
            "handlers": ["stream", "file"],
            "level": logging.INFO,
            "propagate": False
            },
        "root": {
            "handlers": ["stream", "file"],
            "level": logging.INFO,
            "propagate": False
            },
        }
    }
