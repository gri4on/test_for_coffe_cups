# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db.models import get_models
import sys


def report(data, stdout=True, stderr=False, errprefix="Error"):
    """ report helper function """
    if stdout:
        sys.stdout.write(data)
    if stderr:
        assert type(errprefix) == type('')
        sys.stderr.write(errprefix + data)


class Command(BaseCommand):
    help = "Print all models from project"

    def handle(self, *args, **options):
        models = get_models()
        for model in models:
            report("Model name: \'%s\' have %d objects\n" \
                             % (model.__name__, model.objects.count()), \
                                  stdout=True, stderr=True, errprefix="Error: ")