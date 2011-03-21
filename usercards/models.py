from django.db import models
from django.contrib.auth.models import User


class UserCard(models.Model):
    """
    Basic use card
    """
    name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    date_birth = models.DateField(blank=True)
    bio = models.TextField()
    contacts = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    jabber = models.CharField(max_length=256)
    skype = models.CharField(max_length=256)
    other_contacts = models.TextField()


class MiddlewareData(models.Model):
    """
    that class is represent model for request stored in DB
    """
    time = models.DateTimeField(auto_now=True)
    method = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True)
    lang = models.CharField(max_length=255, null=True, blank=True)
    addr = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
