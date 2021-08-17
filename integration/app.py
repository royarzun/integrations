from typing import Dict, List, Tuple, Union

from flask import Flask, jsonify, request

from integration.rest_service.api_client import BaseAPIClient, CodeRequestResponse
from integration.rest_service.exceptions import (
    BadRequest,
    HandledSatelliteException,
    InvalidMembership,
    NotFound,
    UnusableMembership,
)
from integration.rest_service.service import MembershipService


def run_app(cls):
    assert issubclass(
        cls, BaseAPIClient
    ), "API Client class requires to extend from BaseAPIClient class"
    membership_service = MembershipService(api_client=cls())
    app = Flask(__name__)

    @app.route("/authenticate", methods=["POST"])
    def authenticate() -> Tuple[Dict, int]:
        membership_data = membership_service.get_membership_identifier(request.json)
        if not bool(membership_data):
            return {}, 403

        return membership_data, 200

    @app.route("/validate", methods=["POST"])
    def validate() -> Tuple[Dict, int]:
        return (
            jsonify(
                {
                    "is_active": membership_service.is_active(
                        request.json.get("identifier")
                    )
                }
            ),
            200,
        )

    # Own's API's health
    @app.route("/healthz", methods=["GET"])
    def health() -> Tuple[Dict, int]:
        return {}, 200

    # External integration's health
    @app.route("/external_health", methods=["GET"])
    def external_health() -> Tuple[Dict, int]:
        if membership_service.external_service_is_healthy():
            return {}, 200
        return {}, 503

    @app.route("/request_code", methods=["POST"])
    def code_request() -> Tuple[Union[Dict, CodeRequestResponse], int]:
        membership_data = membership_service.request_verification_code(request.json)
        return membership_data, 200

    @app.route("/data/search", methods=["POST"])
    def search_private_identifiers_values() -> Tuple[Union[List[Dict], Dict], int]:
        if request.json and "identifiers" in request.json:
            membership_data = membership_service.search_private_identifiers_values(
                uuids=request.json["identifiers"]
            )
            if len(membership_data["data"]) > 0:
                return membership_data, 200
            raise NotFound
        raise BadRequest

    @app.route("/data/", methods=["POST"])
    def create_private_identifier() -> Tuple[Dict, int]:
        value = request.json.get("value")
        if not value:
            return jsonify({"error": "INVALID_MEMBERSHIP"}), 400
        membership_data = membership_service.create_private_identifier(value)
        return membership_data, 200

    @app.route("/data/<uuid>", methods=["GET"])
    def retrieve_private_identifier(uuid: str) -> Tuple[Dict, int]:
        membership_data = membership_service.get_private_identifier_value(uuid)
        if membership_data:
            return membership_data, 200
        raise NotFound

    @app.route("/data/<uuid>", methods=["DELETE"])
    def delete_private_identifier(uuid: str) -> Tuple[Dict, int]:
        if membership_service.delete_private_identifier(uuid):
            return {}, 200
        raise NotFound

    @app.errorhandler(HandledSatelliteException)
    def handle_exception(e: HandledSatelliteException) -> Tuple[Dict, int]:
        """Return serialized JSON for HandledSatelliteException errors"""
        return jsonify({"error": e.error_code}), e.status_code

    return app
