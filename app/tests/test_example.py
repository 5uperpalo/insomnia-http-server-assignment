import cfg
from src.endpoint_utils import send_request
import unittest.mock as mock

def test_send_request_wrong_url():
    correct_result = {"message": "http server error"}
    assert send_request(cfg.tron_url[:-15], cfg.test_wallet_address) == correct_result

def test_send_request_wrong_address():
    correct_result = {"message": "incorrect wallet address"}
    assert send_request(cfg.tron_url, cfg.test_wallet_address[:-2]) == correct_result

def test_send_request_correct_test_wallet():
    correct_result = {
    "success": True,
    "meta": {
        "at": mock.ANY,
        "page_size": 0,
    },
    "data": [],
    }
    assert send_request(cfg.tron_url, cfg.test_wallet_address) == correct_result
