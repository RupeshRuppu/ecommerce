from json import loads
from django.http import JsonResponse


SUCCESS = "success"
ERROR = "error"


def parse_body(body):
    return loads(body.decode("utf-8"))


def get_success_response(data=None):
    return JsonResponse(
        {
            "status": SUCCESS,
            "data": data,
            "error": None,
        }
    )


def get_error_response(error_message: str = "ERROR"):
    return JsonResponse({"status": ERROR, "data": None, "error": error_message})


def get_method_error(req, supported_method):
    return JsonResponse(
        {
            "status": ERROR,
            "data": None,
            "error": f"{req.method} method is not supported. SUPPORTED METHODS: [{supported_method}]",
        }
    )
