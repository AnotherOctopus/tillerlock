import logging
from typing import Tuple

from flask import Response, jsonify

LOGGER = logging.getLogger(__name__)


def generic_error_handler(error: Exception) -> Tuple[Response, int]:
    """Handle any type of Exception."""
    LOGGER.warning("Error processing request", exc_info=error)
    return (
        jsonify({"error": getattr(error, "description", "internal_error")}),
        getattr(error, "code", 500),
    )
