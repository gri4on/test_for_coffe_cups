# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db.models import get_models
import sys


class Command(BaseCommand):
    help = "Print all models from project"

    def handle(self, *args, **options):
        models = get_models()
        for model in models:
            sys.stdout.write("Model name: \'%s\' have %d objects\n" \
                             % (model.__name__, model.objects.count()))
            sys.stderr.write("Error: Model name: \'%s\' have %d objects\n" \
                             % (model.__name__, model.objects.count()))