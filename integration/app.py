import traceback

from flask import Flask, abort, jsonify, request
from typing import Dict, Union

from integration.rest_service.api_client import BaseAPIClient, CodeRequestResponse
from integration.rest_service.exceptions import InvalidMembership, UnusableMembership
from integration.rest_service.service import MembershipService


def run_app(cls):
    assert issubclass(
        cls, BaseAPIClient
    ), "API Client class requires to extend from BaseAPIClient class"
    membership_service = MembershipService(api_client=cls())
    app = Flask(__name__)

    @app.route("/authenticate", methods=["POST"])
    def authenticate() -> tuple[Dict, int]:
        try:
            membership_data = membership_service.get_membership_identifier(request.json)
            if not bool(membership_data):
                return {}, 403

            return membership_data, 200
        except InvalidMembership:
            return jsonify({"error": "INVALID_MEMBERSHIP"}), 200
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_MEMBERSHIP"}), 200
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    @app.route("/validate", methods=["POST"])
    def validate() -> tuple[Dict, int]:
        try:
            return jsonify(
                {
                    "is_active": membership_service.is_active(
                        request.json.get("identifier")
                    )
                }
            ), 200
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_ACCOUNT"}), 200
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    # Own's API's health
    @app.route("/healthz", methods=["GET"])
    def health() -> tuple[Dict, int]:
        return {}, 200

    # External integration's health
    @app.route("/external_health", methods=["GET"])
    def external_health() -> tuple[Dict, int]:
        if membership_service.external_service_is_healthy():
            return {}, 200
        return {}, 503

    @app.route("/code_request", methods=["POST"])
    def code_request() -> tuple[Union[Dict, CodeRequestResponse], int]:
        try:
            membership_data = membership_service.request_verification_code(request.json)
            return membership_data, 200
        except InvalidMembership:
            return jsonify({"error": "INVALID_MEMBERSHIP"}), 200
        except UnusableMembership:
            return jsonify({"error": "UNUSABLE_MEMBERSHIP"}), 200
        except Exception:
            return jsonify({"error": traceback.format_exc()}), 500

    @app.route("/data/", methods=["POST"])
    def create_private_identifier() -> tuple[Dict, int]:
        value = request.json.get("value")
        if not value:
            return jsonify({"error": "INVALID_MEMBERSHIP"}), 400
        membership_data = membership_service.create_private_identifier(value)
        return membership_data, 200

    @app.route("/data/<uuid>", methods=["GET"])
    def retrieve_private_identifier(uuid: str) -> tuple[Dict, int]:
        membership_data = membership_service.get_private_identifier_value(uuid)
        if membership_data:
            return membership_data, 200
        return jsonify({"error": "NOT_FOUND"}), 404

    @app.route("/data/<uuid>", methods=["DELETE"])
    def delete_private_identifier(uuid: str) -> tuple[Dict, int]:
        if membership_service.delete_private_identifier(uuid):
            return {}, 200
        return jsonify({"error": "NOT_FOUND"}), 404

    return app
