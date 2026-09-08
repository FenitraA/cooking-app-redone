import logging
import uuid

from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def generate_error_id():
    return str(uuid.uuid4())[:8]


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    request = context.get("request")

    # DRF knows how to handle expected API exceptions.
    if response is not None:
        return response

    # Anything that reaches this point is unexpected.
    error_id = generate_error_id()

    logger.exception(
        "Unexpected error [%s] - %s %s",
        error_id,
        request.method if request else "UNKNOWN",
        request.path if request else "UNKNOWN",
    )

    from rest_framework.response import Response
    from rest_framework import status

    return Response(
        {
            "success": False,
            "message": ("Something went wrong on our side. " "Please try again later."),
            "error_id": error_id,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
