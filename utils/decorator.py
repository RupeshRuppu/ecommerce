from jwt import decode
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError
from utils.response import get_error_response
from apis.models import Tokens


def validate_token(func):
    # lot of edge cases to be handled at this decorator.
    def wrapper(*args, **kwargs):
        try:
            request = args[0]
            auth_header = request.headers.get("Authorization")
            if auth_header is None or not isinstance(auth_header, str):
                return get_error_response("Not authorized")
            token = auth_header[7:]

            # check if this token is already black-listed.
            token_instance = Tokens.objects.filter(token__iexact=token).first()

            if token_instance is None:
                return get_error_response("NOT A VALID ACCESS TOKEN")

            if token_instance and token_instance.is_black_listed:
                return get_error_response("TOKEN BLACKLISTED")

            payload = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return func(*args, **kwargs, user_id=payload.get("id"))
        except ExpiredSignatureError:
            return get_error_response("token expired or invalid")
        except Exception as ex:
            return get_error_response(f"{ex.args[0]}")

    return wrapper
