from flask import jsonify, request, Flask

from integration.rest_service.api_client import BaseAPIClient
from integration.rest_service.service import MembershipService


def run_app(cls):
    assert issubclass(
        cls, BaseAPIClient
    ), "API Client class requires to extend from BaseAPIClient class"
    membership_service = MembershipService(api_client=cls())
    app = Flask(__name__)

    @app.route('/authenticate', methods=['POST'])
    def authenticate():
        try:
            membership_data = membership_service.get_membership_identifier(request.json)
            if membership_data is None:
                return {}, 403

            return membership_data
        except:
            return {}, 503

    @app.route('/validate', methods=['POST'])
    def validate():
        try:
            return jsonify(
                {"is_active": membership_service.is_active(request.json)}
            )
        except:
            return {}, 503

    @app.route('/healthz', methods=['GET'])
    def health():
        return {}, 200

    return app
