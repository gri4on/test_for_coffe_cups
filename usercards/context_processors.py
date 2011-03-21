# -*- coding: utf-8 -*-
from django.conf import settings


def settings_processor(request):
    "Creating context proxessor of settings object"
    return {"settings": settings}
