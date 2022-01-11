from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


from .manager import CustomUserManager


class Account(AbstractBaseUser):
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    password = models.CharField(max_length=100, db_column='auth_id')
    last_login = None
    is_superuser = None
    groups = None


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()

    class Meta:
        managed = True
        db_table = 'account'

    def __str__(self):
        return self.username


class PhoneNumber(models.Model):
    number = models.CharField(max_length=40, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'phone_number'
