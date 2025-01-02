from apis.models import User
from datetime import datetime, timedelta, timezone
from django.conf import settings
from jwt import encode

ALGORITHM = "HS256"


def create_token(payload):
    return encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


# access-token:12days & refresh_token:20days
def generate_tokens(user: User, token_exp=10, rtoken_exp=15):
    now = datetime.now(tz=timezone.utc)
    payload = {"id": str(user.id), "username": user.username}
    token = create_token(
        {**payload, "exp": now + timedelta(days=token_exp), "type": "access"}
    )
    rtoken = create_token(
        {**payload, "exp": now + timedelta(days=rtoken_exp), "type": "refresh"}
    )
    return {
        "created_at": now,
        "token": token,
        "rtoken": rtoken,
        "expires_at": now + timedelta(days=rtoken_exp),
    }
