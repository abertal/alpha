import argparse

from django.core.management.base import BaseCommand

from openpyxl import load_workbook

from core import models


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
                'phone_number': data['Teléfono fixo'] or '',
                'mobile_number': data['Teléfono movil'] or '',
                'email': data['Email'] or '',
            }

            membership_data = {
                'membership_fee': data['Cuota socio'] or 0,
                'payment_status': data['Pago'] or '',
                'membership_status': data['Estado'] or '',
            }

            person_membership_data = {
                'id_card_status': data['DNI autorizado'] or '',
                'ss_card_status': data['Tarjeta sanitaria'] or '',
                'photo_status': data['Foto'] or '',
                'dpa_status': data['LOPD'] or '',
            }

            # Group info to determine if this person is a recipient
            group = data['Destinatario'] or ''

            # `card_status´
            por_entregar = data['Carnet entregar'] == 'si'
            entregado = data['Carnet entregado'] == 'si'
            if entregado:
                card_status = 'Entregado'
            elif por_entregar:
                card_status = 'Por entregar'
            else:
                card_status = 'Falta documentación'
            person_membership_data['card_status'] = card_status

            # Store on database
            person, created = models.Person.objects.update_or_create(
                id=data['IdUsuario'],
                defaults=person_data,
            )
            action = 'Creada' if created else 'Actualizada'
            msg = '{} persona con UID {}'.format(action, person.id)
            self.stdout.write(self.style.SUCCESS(msg))

            is_volunteer = data['Voluntario'] == 'si'
            if is_volunteer:
                volunteer, created = models.Volunteer.objects.get_or_create(
                    person=person,
                )
                action = 'Creada' if created else 'Actualizada'
                msg = '{} voluntario con UID {}'.format(action, volunteer.id)
                self.stdout.write(self.style.SUCCESS(msg))

            is_recipient = group.lower() in ['saltimbanqui', 'andaina', 'ads', 'catecumenado']
            if is_recipient:
                recipient, created = models.Recipient.objects.get_or_create(
                    person=person,
                )
                action = 'Creada' if created else 'Actualizada'
                msg = '{} destinatario con UID {}'.format(action, recipient.id)
                self.stdout.write(self.style.SUCCESS(msg))

            mother = data['Madre'] or ''
            if mother:
                mother_person, _ = models.Person.objects.get_or_create(id=mother)
                custodian, created = models.Custodian.objects.update_or_create(
                    person=mother_person,
                    minor=recipient,
                    defaults={'category': 'mother'}
                )
                action = 'Creada' if created else 'Actualizada'
                msg = '{} madre de destinatario {}'.format(action, recipient.id)
                self.stdout.write(self.style.SUCCESS(msg))

            father = data['Padre'] or ''
            if father:
                father_person, _ = models.Person.objects.get_or_create(id=father)
                custodian, created = models.Custodian.objects.update_or_create(
                    person=father_person,
                    minor=recipient,
                    defaults={'category': 'father'}
                )
                action = 'Creada' if created else 'Actualizada'
                msg = '{} padre de destinatario {}'.format(action, recipient.id)
                self.stdout.write(self.style.SUCCESS(msg))

            legal = data['Tutor'] or ''
            if legal:
                legal_person, _ = models.Person.objects.get_or_create(id=legal)
                custodian, created = models.Custodian.objects.update_or_create(
                    person=legal_person,
                    minor=recipient,
                    defaults={'category': 'legal'}
                )
                action = 'Creada' if created else 'Actualizada'
                msg = '{} tutor de destinatario {}'.format(action, recipient.id)
                self.stdout.write(self.style.SUCCESS(msg))

            membership, created = models.Membership.objects.update_or_create(
                id=data['UIDMembresia'],
                defaults=membership_data,
            )
            action = 'Creada' if created else 'Actualizada'
            msg = '{} membresía con UID {}'.format(action, membership.id)
            self.stdout.write(self.style.SUCCESS(msg))

            print('Membership defaults: ', person_membership_data)
            person_membership, created = models.PersonMembership.objects.update_or_create(
                person=person,
                membership=membership,
                defaults=person_membership_data,
            )
            action = 'Creada' if created else 'Actualizada'
            msg = '{} membresía con ID {}'.format(action, person_membership.id)
            self.stdout.write(self.style.SUCCESS(msg))

    def handle(self, *args, **options):
        fp = options['filename']
        wb = load_workbook(fp, read_only=True)
        ws = wb['usuarios']
        self.process_worksheet(ws)
        self.stdout.write(self.style.SUCCESS(
            'Importación finalizada con éxito.'))
