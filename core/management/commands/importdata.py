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
                print('Leída cabecera: ', header)
                continue

            # Regular row
            values = [cell.value for cell in row]

            if not any(values):
                print('Fila {row_number} vacía, seguimos'.format(row_number=row_number))
                continue

            print('Leída fila: ', values)
            data = dict(zip(header, values))
            self.print_row_details(row_number, data)

            # Create or update
            person_data = {
                'name': data['Nome'],
                'surname': data['Apelidos'],
                # 'role': data['Rol'],
                # 'group': data['Grupo'],
                'phone_number': data['Teléfono Fixo'] or '',
                'mobile_number': data['Teléfono Móvil'] or '',
                'email': data['Email'],
            }
            membership_data = {
                # 'uuid': data['IdFamilia'],
                'id_card_status': data['dni autorizado'] or '',
                'ss_card_status': data['tarjeta sanitaria'] or '',
                'photo_status': data['foto'] or '',
                'dpa_status': data['lopd'] or '',
                'membership_fee': data['cuota socio'] or 0,
                'payment_status': data['pago'] or '',
            }

            # `card_status´
            por_entregar = data['Carnet entregar'] == 'si'
            entregado = data['carnet entregado'] == 'si'
            if entregado:
                card_status = 'Entregado'
            elif por_entregar:
                card_status = 'Por entregar'
            else:
                card_status = 'Falta documentación'
            membership_data['card_status'] = card_status

            person, created = models.Person.objects.update_or_create(
                id=data['IdUsuario'],
                defaults=person_data,
            )
            action = 'Creada' if created else 'Actualizada'
            msg = '{} persona con UID {}'.format(action, person.id)
            self.stdout.write(self.style.SUCCESS(msg))

            print('Membership defaults: ', membership_data)
            membership, created = models.Membership.objects.update_or_create(
                person=person,
                defaults=membership_data,
            )
            action = 'Creada' if created else 'Actualizada'
            msg = '{} membresía con ID {}'.format(action, membership.id)
            self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        fp = options['filename']
        wb = load_workbook(fp, read_only=True)
        ws = wb['usuarios']
        self.process_worksheet(ws)
        self.stdout.write(self.style.SUCCESS(
            'Importación finalizada con éxito.'))
