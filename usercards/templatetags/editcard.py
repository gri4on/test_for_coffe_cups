# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse


register = template.Library()


def edit_link(obj):
    """
     Doc: Custom template tag "link_to_admin"
      allow easy to insert link to admin page, to edit object
    """
    return reverse('admin:%s_%s_change' % (obj._meta.app_label, \
                         obj._meta.module_name), args=(obj.pk,))

# Register newly created tag
register.simple_tag(edit_link)