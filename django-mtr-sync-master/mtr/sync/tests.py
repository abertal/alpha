# coding: utf-8

from __future__ import unicode_literals

import os
import datetime

from django.utils.translation import activate

from .lib.manager import Manager
from .models import Settings
from .settings import SETTINGS


class SyncTestMixin(object):
    MODEL = None
    RELATED_MODEL = None
    RELATED_MANY = None
    PROCESSOR = None
    MODEL_COUNT = 30
    CREATE_PROCESSOR_AT_SETUP = True

    def setUp(self):
        self.model = self.MODEL
        self.relatedmodel = self.RELATED_MODEL
        self.manager = Manager()
        self.manager.import_modules(SETTINGS['actions'])

        activate('de')

        self.instance, self.r_instance, self.m_instances = \
            self.model.populate_for_test(self.MODEL_COUNT)

        self.settings = Settings.objects.create(
            action=Settings.EXPORT,
            data_action='create',
            processor=self.PROCESSOR.__name__, worksheet='test',
            model='{}.{}'.format(
                self.model._meta.app_label, self.model.__name__).lower(),
            include_header=False,
            dataset='some_dataset',
            filter_querystring='security_level__gte=10'
            '&surname__icontains=t&o=-3.2&gender__exact=M'
            '&fields=action_checkbox,name,surname,security_level,gender',
            language='de')

        self.queryset = self.manager.get('dataset', 'some_dataset')
        self.queryset = self.queryset(self.MODEL, self.settings)
        self.queryset = self.queryset.filter(
            security_level__gte=10, surname__icontains='t',
            gender__exact='M').order_by('-security_level', 'surname')

        if self.CREATE_PROCESSOR_AT_SETUP:
            self.processor = self.manager.make_processor(self.settings)

            self.fields = self.settings.create_default_fields(add_label=False)


class ProcessorTestMixin(SyncTestMixin):

    def check_file_existence_and_delete(self, report):
        """Delete report file"""

        self.assertIsNone(os.remove(report.buffer_file.path))

    def check_report_success(self, delete=False):
        """Create report from settings and assert it's successful"""

        report = self.manager.export_data(self.settings)

        # report generated
        self.assertEqual(report.status, report.SUCCESS)
        self.assertEqual(report.action, report.EXPORT)
        self.assertIsInstance(report.completed_at, datetime.datetime)

        # file saved
        self.assertTrue(os.path.exists(report.buffer_file.path))
        self.assertTrue(os.path.getsize(report.buffer_file.path) > 0)

        if delete:
            self.check_file_existence_and_delete(report)

        return report

    def test_report_empty_import_errors(self):
        self.settings.start_row = 100
        self.settings.end_row = 350

        report = self.check_report_success()

        self.settings.start_row = 1
        self.settings.end_row = 99
        self.settings.dataset = ''
        self.settings.action = self.settings.IMPORT
        [field.delete() for field in self.settings.fields.all()]
        self.settings.create_default_fields()
        self.settings.buffer_file = report.buffer_file

        report = self.manager.import_data(self.settings)

        self.assertEqual(report.messages.count(), self.settings.end_row)

        self.check_file_existence_and_delete(report)

    def check_sheet_values_and_delete_report(
            self, report, import_report=None, instances=None):
        if import_report:
            self.assertEqual(import_report.status, import_report.SUCCESS)
        else:
            self.assertEqual(report.status, report.SUCCESS)

        if self.settings.start_row:
            start_row = self.settings.start_row - 1
        else:
            start_row = 0

        if self.settings.end_row:
            end_row = self.settings.end_row - 1
        else:
            end_row = self.queryset.count() - 1

        if self.queryset.count() < end_row:
            end_row = self.queryset.count() + start_row - 1
            last = self.queryset.last()
        else:
            last = self.queryset.all()[end_row - start_row]

        first = self.queryset.first()
        if instances:
            first = instances[0]
            last = instances[-1]

        worksheet = self.open_report(report)
        self.check_values(worksheet, first, start_row)

        worksheet = self.open_report(report)
        self.check_values(worksheet, last, end_row)

        self.check_file_existence_and_delete(report)

    def open_report(self, report):
        """Open data file and return worksheet or other data source"""

        raise NotImplementedError

    def check_values(self, worksheet, instance, row, index_prepend=0):
        """Check instance values within data"""

        raise NotImplementedError

    def test_create_export_file_and_report_generation(self):
        self.check_report_success(delete=True)

    def test_export_all_dimension_settings(self):
        self.settings.start_row = 25
        self.settings.end_row = 250

        report = self.check_report_success()

        self.check_sheet_values_and_delete_report(report)

    def test_export_no_dimension_settings(self):
        report = self.check_report_success()

        self.check_sheet_values_and_delete_report(report)

    def test_import_create_data(self):
        self.settings.start_row = 1
        self.settings.end_row = 250

        report = self.check_report_success()

        before = self.settings.end_row - self.settings.start_row + 1
        if before > self.queryset.count():
            before = self.queryset.count()

        self.queryset.delete()
        for tag in self.m_instances:
            tag.delete()

        self.settings.action = self.settings.IMPORT
        self.settings.dataset = ''
        self.settings.buffer_file = report.buffer_file
        self.settings.filter_querystring = ''
        [field.delete() for field in self.settings.fields.all()]
        self.settings.create_default_fields()

        import_report = self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report, import_report)

        self.assertEqual(before, self.queryset.count())

    def test_import_update_data(self):
        report = self.check_report_success()

        self.queryset.update(surname_de='', name_de='')
        self.settings.data_action = 'update'

        self.settings.filter_querystring = ''
        self.settings.buffer_file = report.buffer_file
        self.settings.action = self.settings.IMPORT
        [field.delete() for field in self.settings.fields.all()]
        self.settings.create_default_fields()
        self.settings.fields.filter(attribute='id') \
            .update(find=True, update=False)
        self.settings.dataset = ''

        import_report = self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report, import_report)

    def test_reading_empty_values(self):
        report = self.check_report_success()

        max_rows, max_cols = self.processor.open(report.buffer_file.path)
        self.processor.set_dimensions(
            0, max_rows, max_cols, import_data=True)

        self.assertEqual(
            ['', '', ''], self.processor.read(10000, [0, 23543, 434]))

    def test_import_data_cutsom_dataset_without_model_fields(self):
        self.manager.unregister('dataset', 'custom_data')

        @self.manager.register('dataset')
        def custom_data(model, settings):
            return [[x, y] for x in range(10) for y in range(10)]

        for field in self.settings.fields.all():
            field.delete()

        attrs = []

        self.manager.unregister('action', 'test_import')

        @self.manager.register('action')
        def test_import(model, model_attrs, related_attrs, context, **kwargs):
            attrs.append(model_attrs)

        self.settings.model = ''
        self.settings.filter_querystring = ''
        self.settings.data_action = 'test_import'
        self.settings.dataset = 'custom_data'
        self.settings.action = self.settings.IMPORT
        self.settings.create_default_fields()
        self.settings.fields.create(attribute='test', position='1')

        self.manager.import_data(self.settings)

        self.assertNotEqual(attrs, [])

    def test_import_create_or_update(self):
        self.settings.start_row = 1
        self.settings.end_row = 250

        report = self.check_report_success()

        self.queryset.update(surname_de='', name_de='')

        self.settings.data_action = 'create_or_update'
        self.settings.filter_querystring = ''
        self.settings.buffer_file = report.buffer_file
        self.settings.action = self.settings.IMPORT
        [field.delete() for field in self.settings.fields.all()]
        self.settings.create_default_fields()
        self.settings.fields.filter(attribute__icontains='id') \
            .update(find=True, update=False)
        self.settings.dataset = ''

        import_report = self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report, import_report)
