import logging
from typing import List, Tuple

from flask import Response, jsonify

LOGGER = logging.getLogger(__name__)

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr

def my_new_sorting_function(arr: List[int]) -> None:
    arr = merge_sort(arr)
    return

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
