from django.conf import settings
from jwt import decode
from jwt.exceptions import ExpiredSignatureError

from apis.models import Tokens
from utils.constants import HttpStatus, TokenStatus
from utils.response import get_error_response


def validate_token(func):
    """
    This decorator is used to validate the access token.
    """

    def wrapper(*args, **kwargs):
        try:
            request = args[0]
            auth_header = request.headers.get("Authorization")
            if auth_header is None or not isinstance(auth_header, str):
                return get_error_response(HttpStatus.UNAUTHORIZED.name, 401)
            token = auth_header[7:]

            # check if this token is already black-listed.
            token_ins = Tokens.objects.filter(token__iexact=token).first()

            if token_ins is None:
                return get_error_response(TokenStatus.INVALID.name, 401)

            if token_ins and token_ins.is_black_listed:
                return get_error_response(TokenStatus.BLAKLISTED.name, 401)

            payload = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return func(*args, **kwargs, user_id=payload.get("id"))
        except ExpiredSignatureError:
            return get_error_response(TokenStatus.EXPIRED.name, 401)
        except Exception as ex:
            return get_error_response(f"{ex.args[0]}")

    return wrapper
