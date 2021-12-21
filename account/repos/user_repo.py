from django.db import models
from account.models import User


def get(pk):
    try:
        return User.objects.get(pk=pk)
    except models.ObjectDoesNotExist:
        return None


def filter_(**kwargs):
    return User.objects.filter(**kwargs)


def create(
    email, username, first_name, last_name=""
):
    kwargs = locals().copy()
    return User.objects.create(**kwargs)
