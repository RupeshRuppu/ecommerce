from json import loads

from django.http import JsonResponse

from utils.constants import HttpStatus, ResponseStatus


def parse_body(body):
    return loads(body.decode("utf-8"))


def get_success_response(data=None, status=HttpStatus.OK.value):
    return JsonResponse(
        {
            "status": ResponseStatus.SUCCESS.value,
            "data": data,
            "error": None,
        },
        status=status,
    )


def get_error_response(
    error_message: str = "ERROR", status=HttpStatus.INTERNAL_SERVER_ERROR.value
):
    return JsonResponse(
        {"status": ResponseStatus.ERROR.value, "data": None, "error": error_message},
        status=status,
    )


def get_method_error(req, supported_method):
    return JsonResponse(
        {
            "status": ResponseStatus.ERROR.value,
            "data": None,
            "error": f"{req.method} method is not supported. SUPPORTED METHODS: [{supported_method}]",
        },
        status=HttpStatus.BAD_REQUEST.value,
    )
