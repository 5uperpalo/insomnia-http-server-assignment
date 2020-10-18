from flask import Flask, jsonify, request, abort
from functools import wraps
from flask_restful import Api, Resource
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from src.endpoint_utils import send_request
import logging
from logging.config import dictConfig
import pdb
import psutil
import platform
import datetime
import cfg
import flask_profiler

dictConfig(cfg.logging_config)
logger = logging.getLogger(__name__)

# initialize app and api
app = Flask("InsomniaHTTP")
app.config["DEBUG"] = True
app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {"engine": "sqlite"},
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "admin"
        },
    }

api = Api(app)


# authentication
# from https://coderwall.com/p/4qickw/require-an-api-key-for-a-route-in-flask-using-only-a-decorator
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get("key") and request.headers.get("key") == cfg.API_key: # noqa
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def check_inputdata(request):
    """Check if input data is in valid json format

    Args:
        request: client HTTP GET request

    Returns:
        dict: values inside HTTP GET(JSON) request

    """
    if request.is_json is True:
        posted_data = request.get_json()
        validate(instance=posted_data, schema=cfg.client_input_schema)
        return posted_data
    else:
        raise TypeError


class HealthCheck(Resource):
    """/api/healtcheck - returns the health of the service, performs various
    checks, such as the status of the connections to the infrastructure
    services used by the service instance the status of the host, e.g. disk
    space application specific logic.

    Args:
        NA

    Returns:
        JSON(dict): values containing health of the container
    """
    def get(self):
        UsagePerCPU = psutil.cpu_percent(percpu=True)
        ActiveCPU = len(list(filter(lambda x: x >= 0, UsagePerCPU)))
        return jsonify({
            "operation_memory_usage": psutil.virtual_memory()._asdict()["percent"], # noqa
            "disk_space_usage": psutil.disk_usage("/")._asdict()["percent"],
            "cpu_usage": psutil.cpu_percent(),
            "num_of_cores": psutil.cpu_count(),
            "num_of_active_cores ": ActiveCPU,
            "server_wake_time": (datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds(), # noqa
            "free_operation_memory": psutil.virtual_memory()._asdict()["free"],
            "free_disk_space": psutil.disk_usage("/")._asdict()["free"],
            "os": [platform.system(), platform.version()]
            })


class TronWallet(Resource):
    """/api/tronwallet - endpoint that returns status of your tron wallet

    Args:
        JSON(dict): wallet address

    Returns:
        JSON(dict): wallet information
    """

    @require_appkey
    def get(self):
        try:
            posted_data = check_inputdata(request)
            result = send_request(cfg.tron_url, posted_data["address"])
            return jsonify(result)

        except TypeError:
            logger.info("client input not json")
            return jsonify({"message": "client input not json"})

        except ValidationError:
            logger.info("client input validation error:", exc_info=True)
            return jsonify({"message": "client input validation error"})

        except Exception:
            logger.info("error:", exc_info=True)
            return jsonify({"message": "error"})
    pass


api.add_resource(HealthCheck, "/api/health")
api.add_resource(TronWallet, "/api/wallet")
flask_profiler.init_app(app)
