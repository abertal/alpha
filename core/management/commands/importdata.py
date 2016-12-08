import argparse

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importa datos desde un archivo.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('rb'))

    def handle(self, *args, **options):
        fp = options['filename']
        for _ in fp:
            print('.', end='')
        self.stdout.write(self.style.SUCCESS('Importación finalizada con éxito.'))
