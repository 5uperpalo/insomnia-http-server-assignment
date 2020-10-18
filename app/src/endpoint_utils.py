from jsonschema import validate
from jsonschema.exceptions import ValidationError
import logging
import pdb
import cfg
import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError

logger = logging.getLogger(__name__)


def send_request(url, address):
    """Send request function.

    Args:
        address(str): wallet address
        url(str): tron url

    Returns:
        dict: response from Tron API
    """
    try:
        response = requests.get(url + address)
        returned_data = response.json()
        if returned_data["success"] is False:
            raise ValueError
        validate(instance=returned_data, schema=cfg.server_response_schema)
        return returned_data

    except (Timeout, HTTPError, ConnectionError):
        logger.info("http server error:", exc_info=True)
        return {"message": "http server error"}

    except ValueError:
        logger.info("incorrect wallet address")
        return {"message": "incorrect wallet address"}

    except ValidationError:
        logger.info("http server output validation error:", exc_info=True)
        return {"message": "http server output validation error"}

    except Exception:
        logger.info("error:", exc_info=True)
        return {"message": "error"}
