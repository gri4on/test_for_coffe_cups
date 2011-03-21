# -*- coding: utf-8 -*-
from django.forms import ModelForm
from test_for_coffe_cups.usercards.models import UserCard
import settings
from django import forms


class CalendarWidget(forms.TextInput):
    class Media:
        js = (
        settings.MEDIA_URL + 'js/jquery-1.4.4.min.js',
        settings.MEDIA_URL + 'js/jquery-ui-1.8.10.custom.min.js',
        settings.MEDIA_URL + 'jquery.form.js',
        )
        css = {
            'all': (
            settings.MEDIA_URL + "css/smoothness/jquery-ui-1.8.10.custom.css",
            )
        }


    def __init__(self, attrs={}):
        super(CalendarWidget, self).__init__(attrs={'class': 'vDateField',
                                                    'size': '10'})


class CardForm(ModelForm):
    class Meta:
        model = UserCard
        widgets = {
            'date_birth': CalendarWidget
        }
