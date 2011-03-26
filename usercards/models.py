# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Message



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


class ObjectsChanged(models.Model):
    """
    that class represent model of changes in other models (task#10)
    """
    time_stamp = models.DateTimeField(auto_now=True)
    model_object = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    action_name = models.CharField(max_length=20)


def action_callback(sender, **kwargs):
    # Remove recursion - don`t handle ObjectChanged
    # and objects that don`t need to be reported
    
    if sender in [ObjectsChanged, Session, \
                  Message, MiddlewareData]:
        return

    # Don`t have signal which is don`t have 'created'
    if 'created' not in kwargs.keys():
        return

    ACTIONS_NAMES = {None: 'delete', \
                 True: 'create', \
                False: 'edit'}

    content_type = ContentType.objects.get_for_model(sender)
    ObjectsChanged.objects.create(model_object = content_type, \
                                  object_id = kwargs['instance'].id, \
                                  action_name = ACTIONS_NAMES[kwargs['created']])


signals.post_save.connect(action_callback)
signals.post_delete.connect(action_callback)