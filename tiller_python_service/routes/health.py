from flask import Blueprint


blueprint = Blueprint("health", __name__)


@blueprint.route("/health", methods=("GET",))
def get_health():
    return {"status": "all good"}


@blueprint.route("/unhealth", methods=("GET",))
def get_unhealth():
    raise Exception("uh oh")