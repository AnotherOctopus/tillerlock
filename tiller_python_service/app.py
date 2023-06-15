import logging

from flask import Flask, Response
from routes import health, pull_request
from error_handlers import validation_error_handler, generic_error_handler, ValidationError


app = Flask(__name__)
app.register_blueprint(health.blueprint, url_prefix="/v1")
app.register_blueprint(pull_request.blueprint, url_prefix="/v1")
app.register_error_handler(ValidationError, validation_error_handler)
app.register_error_handler(Exception, generic_error_handler)
