from flask import jsonify, request

from integration.rest_service.settings import run

app, membership_service = run()


@app.route("/authenticate", methods=["POST"])
def authenticate():
    try:
        membership_data = membership_service.get_membership_identifier(
            jsonify(request.data)
        )
        if membership_data is None:
            return {}, 403

        return jsonify(membership_data)
    except:
        return {}, 503


@app.route("/validate", methods=["POST"])
def validate():
    try:
        return jsonify(
            {"is_active": membership_service.is_active(jsonify(request.data))}
        )
    except:
        return {}, 503
