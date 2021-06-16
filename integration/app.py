import traceback

from flask import Flask, abort, jsonify, request

from integration.rest_service.api_client import BaseAPIClient
from integration.rest_service.exceptions import InvalidMembership, UnusableMembership
from integration.rest_service.service import MembershipService


def run_app(cls):
    assert issubclass(
        cls, BaseAPIClient
    ), "API Client class requires to extend from BaseAPIClient class"
    membership_service = MembershipService(api_client=cls())
    app = Flask(__name__)

    @app.route("/authenticate", methods=["POST"])
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

    @app.route("/validate", methods=["POST"])
    def validate():
        try:
            return jsonify(
                {
                    "is_active": membership_service.is_active(
                        request.json.get("identifier")
                    )
                }
            )
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_ACCOUNT"})
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    # Own's API's health
    @app.route("/healthz", methods=["GET"])
    def health():
        return {}, 200

    # External integration's health
    @app.route("/external_health", methods=["GET"])
    def external_health():
        if membership_service.external_service_is_healthy():
            return {}, 200
        return {}, 503

    @app.route("/code_request", methods=["POST"])
    def code_request():
        try:
            membership_data = membership_service.request_verification_code(request.json)
            return membership_data
        except InvalidMembership:
            return jsonify({"error": "INVALID_MEMBERSHIP"})
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_MEMBERSHIP"})
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    @app.route("/data/", methods=["POST"])
    def create_private_identifier():
        value = request.json.get("value")
        if not value:
            return jsonify({"error": "INVALID_MEMBERSHIP"}), 400
        membership_data = membership_service.create_private_identifier(value)
        return membership_data

    @app.route("/data/<uuid>", methods=["GET"])
    def retrieve_private_identifier(uuid):
        membership_data = membership_service.get_private_identifier_value(uuid)
        if membership_data:
            return membership_data
        return jsonify({"error": "NOT_FOUND"}), 404

    @app.route("/data/<uuid>", methods=["DELETE"])
    def delete_private_identifier(uuid):
        if membership_service.delete_private_identifier(uuid):
            return {}, 200
        return jsonify({"error": "NOT_FOUND"}), 404

    return app
