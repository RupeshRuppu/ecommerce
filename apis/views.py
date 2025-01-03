from utils.response import get_error_response, get_success_response, get_method_error
from django.views.decorators.csrf import csrf_exempt
from utils.decorator import validate_token
from apis.models import User
from cloudinary.uploader import upload
from django.views.decorators.csrf import csrf_exempt
from utils.response import (
    get_error_response,
    get_success_response,
    get_method_error,
    parse_body,
)
from apis.models import User, Tokens
from django.core.exceptions import ObjectDoesNotExist
from utils.jwt import generate_tokens
from django.db.models import Q
from jwt import decode
from jwt.exceptions import ExpiredSignatureError
from django.conf import settings
import json
from utils.constants import LoginStatus, TokenStatus


@csrf_exempt
def register(req):
    """
    This view is used to register a new user.
    """
    if req.method == "POST":
        try:
            body = parse_body(req.body)
            username, password = body.get("username"), body.get("password")
            # check if a user already exists with these credentials.
            try:
                User.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                return get_error_response(LoginStatus.USER_ALREADY_EXISTS.value)
            except ObjectDoesNotExist:
                user = User(**body, email=username)
                user.set_password(password)

                # generate tokens
                payload = generate_tokens(user)
                token = Tokens(
                    created_at=payload["created_at"],
                    expires_at=payload["expires_at"],
                    token=payload["token"],
                    refresh_token=payload["rtoken"],
                    user=user,
                )

                user.save()
                token.save()
                return get_success_response(
                    {
                        "access_token": payload["token"],
                        "refresh_token": payload["rtoken"],
                    }
                )

        except Exception as ex:
            return get_error_response((json.dumps(ex.args)))
    else:
        return get_method_error(req, "POST")


@csrf_exempt
def login(req):
    """
    This view is used to login a user.
    """
    if req.method == "POST":
        try:
            body = parse_body(req.body)
            username, password = body.get("username"), body.get("password")

            # check if a user exists.
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )

            # validate his password.
            check = user.check_password(password)
            if not check:
                return get_error_response(LoginStatus.INVALID_PASSWORD.value)

            payload = generate_tokens(user)
            token = Tokens(
                created_at=payload["created_at"],
                expires_at=payload["expires_at"],
                token=payload["token"],
                refresh_token=payload["rtoken"],
                user=user,
            )
            token.save()
            return get_success_response(
                {
                    "access_token": payload["token"],
                    "refresh_token": payload["rtoken"],
                }
            )

        except ObjectDoesNotExist:
            return get_error_response(LoginStatus.USER_NOT_EXISTS.value)

        except Exception as ex:
            return get_error_response((json.dumps(ex.args)))
    else:
        return get_method_error(req, "POST")


@csrf_exempt
def refresh_token(req):
    """
    This view is used to refresh the access token.
    """
    if req.method == "POST":
        try:
            body = parse_body(req.body)
            refresh_token = body.get("refresh_token")

            if refresh_token is None:
                return get_error_response("NO REFRESH TOKEN PROVIDED IN BODY")

            # check the refresh_token is black-listed
            rf_token = Tokens.objects.filter(
                refresh_token__iexact=refresh_token
            ).first()

            if rf_token is None:
                return get_error_response(TokenStatus.NOT_A_VALID_REFRESH_TOKEN.name)

            if rf_token and rf_token.is_black_listed:
                return get_error_response(TokenStatus.BLAKLISTED.name)

            # validate token.
            payload = decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

            rf_token.is_black_listed = True
            user = User.objects.get(id=payload["id"])
            payload = generate_tokens(user)
            token = Tokens(
                created_at=payload["created_at"],
                expires_at=payload["expires_at"],
                token=payload["token"],
                refresh_token=payload["rtoken"],
                user=user,
            )
            rf_token.save()
            token.save()
            return get_success_response(
                {
                    "access_token": payload["token"],
                    "refresh_token": payload["rtoken"],
                }
            )

        except ObjectDoesNotExist:
            return get_error_response(TokenStatus.NOT_A_VALID_REFRESH_TOKEN.name)

        except ExpiredSignatureError:
            return get_error_response(TokenStatus.NOT_A_VALID_REFRESH_TOKEN.name)

        except Exception as ex:
            return get_error_response((json.dumps(ex.args)))
    else:
        return get_method_error(req, "POST")


# Create your views here.
@csrf_exempt
@validate_token
def profile_upload(*args, **kwargs):
    """
    This view is used to upload the profile image of the user.
    """
    req, user_id = args[0], kwargs["user_id"]
    if req.method == "POST":
        try:
            # Get image files from the req.FILES
            image = req.FILES.get("image")
            if image is None:
                return get_error_response("No image data found!")
            result = upload(image, public_id=user_id, folder="user-profiles")
            user = User.objects.get(id=user_id)
            user.profile_url = result["secure_url"]
            user.save()
            return get_success_response({"url": result["secure_url"]})

        except Exception as e:
            return get_error_response(str(e.args[0]))
    else:
        return get_method_error(req, "POST")


# TODO : category comes from UI and upload under those folder.
# TODO : user_id(which admin/ops) member has uploaded this product?
@csrf_exempt
@validate_token
def product_upload(*args, **kwargs):
    """
    This view is used to upload the product images.
    """
    req, user_id = args[0], kwargs["user_id"]
    if req.method == "POST":
        try:
            # Get image files from the req.FILES
            images = list(filter(lambda img: img, req.FILES.getlist("images")))
            category, result = req.POST.get("category"), []
            for image in images:
                response = upload(image, folder=f"e-commerce-products/{category}")
                result.append(response["secure_url"])
            return get_success_response({"uploaded_files": result})

        except Exception as e:
            return get_error_response(str(e.args[0]))
    else:
        return get_method_error(req, "POST")
