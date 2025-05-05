from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


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
    user = models.ForeignKey("apis.User", on_delete=models.CASCADE)
    is_black_listed = models.BooleanField(default=False)

    class Meta:
        db_table = "tokens"

    def __str__(self) -> str:
        return f"{self.user_id.id}:{self.refresh_token}"


class Product(models.Model):
    """
    This model is used to store the product details.
    # image_url is going to store the URL of the image uploaded by the user. :colon seperated.
    """

    choices = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    size = models.CharField(max_length=255, null=True, choices=choices)
    color = models.CharField(max_length=255, null=True)
    stock_quantity = models.IntegerField(default=0, null=False)
    category = models.ForeignKey("apis.Category", on_delete=models.SET_NULL, null=True)
    rating = models.ForeignKey(
        "apis.Rating",
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_rating",
    )
    image_url = models.TextField(null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"

        def __str__(self) -> str:
            return self.name


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    score = models.DecimalField(max_digits=3, decimal_places=2, null=False)
    rating_count = models.IntegerField(default=0, null=False)
    user = models.ForeignKey("apis.User", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "apis.Product", on_delete=models.CASCADE, related_name="rating_product"
    )

    class Meta:
        db_table = "ratings"

    def __str__(self) -> str:
        return f"{self.product.name} - {self.rating}"


class Favorites(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey("apis.User", on_delete=models.CASCADE)
    product = models.ForeignKey("apis.Product", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wishlist"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.product.name}"
