import logging
from typing import Tuple

from flask import Response, jsonify

LOGGER = logging.getLogger(__name__)

def my_new_sorting_function(arr):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n-1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
         
        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return

def my_new_sorting_function(arr):
    return sorted(arr)

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
