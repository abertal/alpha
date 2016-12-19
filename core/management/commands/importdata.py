import argparse

from django.core.management.base import BaseCommand

from core import models

from openpyxl import load_workbook


class Command(BaseCommand):
    help = 'Importa datos desde un archivo.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('rb'))
        
    def print_row_details(self, row_number, data):
        print('-- Línea {row_number}'.format(row_number=row_number))
        for key, value in data.items():
            print('Columna `{key}`: {value!r}'.format(key=key, value=value))

    def process_worksheet(self, ws):
        header = None
        for row_number, row in enumerate(ws.rows, 1):
            # Row 1 to 3 are empty
            if row_number in [1, 2, 3]:
                continue
            
            # First row contains the headers
            if not header:
                header = [cell.value for cell in row]
                continue
            values = [cell.value for cell in row]
            print('cadena values')
            print(values)
            data = dict(zip(header, values))
            print('cadena len')
            print(len(data))
            self.print_row_details(row_number, data)

            # Create or update
            defaults = {
                'uuid': data['IdFamilia'],
                'name': data['Nome'],
                'surname': data['Apelidos'],
                'role': data['Rol'],
                'group': data['Grupo'],
                'phone_number': data['Telefono fixo'],
                'mobile_number': data['Telefono movil'],
                'email': data['Email'],
                'id_card': data['DNI autorizado'],
                'ss_card': data['Tarjeta sanitaria'],
                'photo': data['Foto'],
                'DPA': data['LOPD'],
                'membership_fee': data['Cuota socio'],
                'membership_payment': data['Pago'],
                'done_idmembership': data['Carnet para entregar'],
                'delivered_idmembership': data['Carnet entregado'],
            }

            membership, created = models.Membership.object.update_or_create(
                id=data['IdUsuario'],
                defaults=defaults,
            )
            action = 'Creada' if created else 'Actualizada'
            msg = '{} persona con UID {}'.format(action, membership.id)
            self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        fp = options['filename']
        print('cadena fp')
        print(fp)
        wb = load_workbook(fp, read_only=True)
        ws = wb['usuarios']
        self.process_worksheet(ws)
        self.stdout.write(self.style.SUCCESS(
            'Importación finalizada con éxito.'))
