from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import os
import random
#import requests


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('User must have a phone number')
        if not password:
            raise ValueError('User must provide a password')

        user_obj = self.model(
            phone = phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password = password,
            is_staff= True
        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user



class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be in a 10 digit +233XXXXXXXX format")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name = models.CharField(max_length=100, blank= True, null=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    street_name = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    registered_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.phone
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="PHone number mut be entered in the format +233XXXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number Of OTP sent')
    validated = models.BooleanField(default= False, help_text='If it is checked, it means user have validated their phone number')


    def __str__(self):
        return str(self.otp) + " is sent to " + str(self.phone)



class UserBase(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)

    class Meta:
        abstract = True
        ordering = ['last_name']


"""     avatar = ProcessedImageField(
        upload_to='profile_pics',
        processors=[ResizeToFill(100,50)],
        format='JPEG',
        options={'quality': 60 }
    ) """