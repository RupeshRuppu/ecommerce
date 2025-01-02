from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    profile_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return f"{self.id},{self.username}"


class Tokens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(blank=False, null=False)
    expires_at = models.DateTimeField(blank=False, null=False)
    token = models.TextField(null=False, blank=False)
    refresh_token = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_black_listed = models.BooleanField(default=False)

    class Meta:
        db_table = "tokens"

    def __str__(self) -> str:
        return f"{self.user_id.id}:{self.refresh_token}"
