import logging
from flask import Blueprint, request

from error_handlers import ValidationError


blueprint = Blueprint("pull_request", __name__)


@blueprint.route("/pull-request", methods=("POST",))
def update():
    json_data = request.get_json()
    if not json_data:
        raise ValidationError("Request body not supplied")

    # pass json_data wherever

    return {"status": "success"}
