from django.db import models
from utils.choice import Choice
from ride.models import VehicleType
from django.contrib.postgres.fields import JSONField


class CouponStatus(Choice):
    ACTIVE = 1
    INACTIVE = 2


class CouponDiscountType(Choice):
    FLAT = 1
    PERCENTAGE = 2


class Coupon(models.Model):
    expires_at = models.DateTimeField()
    value = models.PositiveIntegerField()
    code = models.CharField(max_length=16, unique=True)

    status = models.PositiveIntegerField(
        choices=CouponStatus.choices(), default=CouponStatus.ACTIVE.value
    )
    dType = models.PositiveIntegerField(
        choices=CouponDiscountType.choices(), default=CouponDiscountType.FLAT.value
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class PricingStrategy(models.Model):
    strategy = JSONField(default=dict)
    vType = models.PositiveIntegerField(
        choices=VehicleType.choices(), default=VehicleType.SEDAN.value, db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
