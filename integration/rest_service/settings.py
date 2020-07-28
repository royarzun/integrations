from importlib import import_module
from os import getenv

from flask import Flask

from integration.rest_service.api_client import BaseAPIClient
from integration.rest_service.exceptions import ImproperlyConfigured
from integration.rest_service.service import MembershipService


INTEGRATION_API_CLIENT_CLASS_SETTING = "INTEGRATION_API_CLIENT_CLASS"


def run():
    app = Flask(__name__)
    env_class_dot_path = getenv(INTEGRATION_API_CLIENT_CLASS_SETTING)
    if env_class_dot_path is None:
        raise ImproperlyConfigured(
            "INTEGRATION_API_CLIENT_CLASS_SETTING setting is required!!!"
        )
    module = import_module(env_class_dot_path)
    class_name = env_class_dot_path.split(".")[-1]
    api_client_class = getattr(module, class_name)
    assert issubclass(
        api_client_class, BaseAPIClient
    ), "API Client class requires to extend from BaseAPIClient class"

    return app, MembershipService(api_client=api_client_class())
