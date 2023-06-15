import logging
from typing import Tuple

from flask import Response, jsonify

LOGGER = logging.getLogger(__name__)


class ValidationError(Exception):
    pass


def validation_error_handler(error: ValidationError) -> Tuple[Response, int]:
    """Handle any type of Exception."""
    LOGGER.warning("Validation error processing request", exc_info=error)
    return (
        jsonify({"error": error.args[0]}),
        getattr(error, "code", 400),
    )


def generic_error_handler(error: Exception) -> Tuple[Response, int]:
    """Handle any type of Exception."""
    LOGGER.warning("Error processing request", exc_info=error)
    return (
        jsonify({"error": getattr(error, "description", "internal_error")}),
        getattr(error, "code", 500),
    )
