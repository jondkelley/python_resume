import pytest
from time import sleep
from os import environ

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]


@pytest.fixture
def update_secret():
    yield environ.get('UPDATE_SECRET')


@pytest.fixture(scope="function")
def wait_for_flask(function_scoped_container_getter):
    """Wait for the flask app to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    pandoc_container = function_scoped_container_getter.get("pandoc2")
    service = function_scoped_container_getter.get("resume2").network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    return request_session, api_url
