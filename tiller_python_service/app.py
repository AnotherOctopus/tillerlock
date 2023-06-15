import logging

from flask import Flask, Response
from routes import health
from error_handlers import generic_error_handler


app = Flask(__name__)
app.register_blueprint(health.blueprint, url_prefix="/v1")
app.register_error_handler(Exception, generic_error_handler)
