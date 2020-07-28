from flask import jsonify, request, Flask

from integration.rest_service.api_client import BaseAPIClient
from integration.rest_service.service import MembershipService


def run_app(cls):
    assert issubclass(
        cls, BaseAPIClient
    ), "API Client class requires to extend from BaseAPIClient class"
    membership_service = MembershipService(api_client=cls())
    app = Flask(__name__)

    def authenticate():
        try:
            membership_data = membership_service.get_membership_identifier(request.data)
            if membership_data is None:
                return {}, 403

            return membership_data
        except:
            return {}, 503

    def validate():
        try:
            return jsonify(
                {"is_active": membership_service.is_active(request.data)}
            )
        except:
            return {}, 503

    app.add_url_rule("/authenticate", "/authenticate", view_func=authenticate)
    app.add_url_rule("/validate", "/validate", view_func=validate)
    app.route(methods=["post"], rule=None)
    return app
