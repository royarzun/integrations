import traceback

from flask import jsonify, request, Flask

from integration.rest_service.api_client import BaseAPIClient
from integration.rest_service.exceptions import UnusableMembership, InvalidMembership
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
            if not bool(membership_data):
                return {}, 403

            return membership_data
        except InvalidMembership:
            return jsonify({"error": "INVALID_MEMBERSHIP"})
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_MEMBERSHIP"})
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    @app.route('/validate', methods=['POST'])
    def validate():
        try:
            return jsonify(
                {"is_active": membership_service.is_active(request.json.get("identifier"))}
            )
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_ACCOUNT"})
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    # Own's API's health
    @app.route('/healthz', methods=['GET'])
    def health():
        return {}, 200

    # External integration's health
    @app.route('/external_health', methods=['GET'])
    def external_health():
        if membership_service.external_service_is_healthy():
            return {}, 200
        return {}, 503

    return app
