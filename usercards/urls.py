# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('usercards.views',
    url(r'^$', "contact", name='contact_home'),
    url(r'^edit_usercard/$', "edit_card", name='card_edit'),
    url(r'^middleware/$', "report_middleware", name='midl_report'),
    url(r'^ctx_proc/$', "context_processor", name='ctx_proc'),
)
