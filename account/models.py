from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from utils.choice import Choice


class RoleEnum(Choice):
    DRIVER = 1
    RIDER = 2


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(User, self).save(*args, **kwargs)
        if created:
            if self.is_role_set() is False:
                self.make_rider()

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def role(self):
        return self.groups.filter(user=self).first().name

    def is_role_set(self):
        return self.groups.filter(name__in=[role.value for role in RoleEnum]).exists()

    def is_driver(self):
        return self.groups.filter(name=RoleEnum.DRIVER.value).exists()

    def is_rider(self):
        return self.groups.filter(name=RoleEnum.RIDER.value).exists()

    def make_rider(self):
        group = Group.objects.get(name=RoleEnum.RIDER.value)
        self.groups.set([group])
        return self

    def make_driver(self):
        group = Group.objects.get(name=RoleEnum.DRIVER.value)
        self.groups.set([group])
        return self

    def set_user_role(self, role):
        if role == RoleEnum.DRIVER.value:
            self.make_driver()
        elif role == RoleEnum.RIDER.value:
            self.make_rider()
        else:
            raise Exception("No role like {role} found".format(role=role))


class TripStatus(Choice):
    AWAITING = 1
    ONGOING = 2
    COMPLETED = 3


class Trip(models.Model):
    price = models.PositiveIntegerField()
    status = models.PositiveIntegerField(
        choices=TripStatus.choices(), default=TripStatus.AWAITING.value
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    rider = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="rider_trips")
    driver = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="driver_trips")
