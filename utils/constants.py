from enum import Enum


class TokenStatus(Enum):
    INVALID = "INVALID"
    EXPIRED = "EXPIRED"
    BLAKLISTED = "BLACKLISTED"
    NOT_A_VALID_REFRESH_TOKEN = "NOT A VALID REFRESH TOKEN"


class HttpStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    UNAUTHORIZED = 401
    BAD_REQUEST = 400


class ResponseStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class LoginStatus(Enum):
    INVALID_PASSWORD = "INVALID PASSWORD"
    USER_NOT_EXISTS = "USER NOT EXISTS"
    USER_ALREADY_EXISTS = "USER ALREADY EXISTS"


class ProductItem(Enum):
    REQUIRED_FIELDS = [
        "id",
        "name",
        "price",
        "image_url",
        "description",
        "size",
        "color",
        "category_id",
    ]
