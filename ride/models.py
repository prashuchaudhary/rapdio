from django.db import models
from utils.choice import Choice


class VehicleStatus(Choice):
    VACANT = 1
    OCCUPIED = 2


class VehicleType(Choice):
    SEDAN = 1
    HATCHBACK = 2


class Vehicle(models.Model):
    registration_number = models.CharField(max_length=16, unique=True)
    vType = models.PositiveIntegerField(
        choices=VehicleType.choices(), default=VehicleType.SEDAN.value, db_index=True
    )
    status = models.PositiveIntegerField(
        choices=VehicleStatus.choices(), default=VehicleStatus.VACANT.value, db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class VehicleLocation(models.Model):
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    long = models.DecimalField(max_digits=8, decimal_places=6)
