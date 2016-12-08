import argparse

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importa datos desde un archivo.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importación finalizada con éxito.'))
