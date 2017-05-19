from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings as django_settings

from .settings import SETTINGS, strip_media_root
from .translation import gettext_lazy as _
from .lib.helpers import model_attributes
from .lib.signals import export_started, export_completed, \
    import_started, import_completed, error_raised
from .lib.exceptions import ErrorChoicesMixin

from mtr.utils.models.mixins import PositionRelatedMixin, \
    TimeStampedMixin


class ExportManager(models.Manager):

    """Shortcut for export queryset"""

    def get_queryset(self):
        return super(ExportManager, self).get_queryset() \
            .filter(action=self.model.EXPORT)


class ImportManager(models.Manager):

    """Shortcut for import queryset"""

    def get_queryset(self):
        return super(ImportManager, self).get_queryset() \
            .filter(action=self.model.IMPORT)


class RunningManager(models.Manager):

    """Shortcut for running Report entry queryset"""

    def get_queryset(self):
        return super(RunningManager, self).get_queryset() \
            .filter(status=self.model.RUNNING)


class ActionsMixin(models.Model):

    """Action choices mixin"""

    EXPORT = 0
    IMPORT = 1

    ACTION_CHOICES = (
        (EXPORT, _('Export')),
        (IMPORT, _('Import'))
    )

    action = models.PositiveSmallIntegerField(
        _('action'), choices=ACTION_CHOICES, db_index=True, default=EXPORT)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Settings(ActionsMixin, TimeStampedMixin):

    """Settings for imported and exported files"""

    name = models.CharField(
        _('name'), blank=True, max_length=100,
        help_text=_('Small description of operation'))

    start_row = models.PositiveIntegerField(
        _('start row'), null=True, blank=True,
        help_text=_("Reading or writing start index (including itself)"))

    end_row = models.PositiveIntegerField(
        _('end row'), null=True, blank=True,
        help_text=_("Reading or writing end index (including itself)"))

    model = models.CharField(
        _('model'), max_length=255, blank=True,
        help_text=_("Choose database model if action need it"))

    show_in_quick_menu = models.BooleanField(
        _('show in quick menu list'), default=False)

    processor = models.CharField(
        _('format'), max_length=255,
        default=SETTINGS['default_processor'],
        help_text=_("Choose file type"))
    worksheet = models.CharField(
        _('worksheet page'), max_length=255, blank=True,
        help_text=_("Page name of sheet book"))
    include_header = models.BooleanField(
        _('include header'), default=True,
        help_text=_(
            "Check it if you need to write field names in"
            " export or skip it in import"))

    filename = models.CharField(
        _('custom filename'), max_length=255, blank=True,
        help_text=_("Custom filename for export"))
    buffer_file = models.FileField(
        _('file'), upload_to=SETTINGS['path'], db_index=True, blank=True,
        help_text=_("File for import action"))

    dataset = models.CharField(
        _('dataset'), max_length=255, blank=True,
        help_text=_(
            "Custom registered dataset if you import or export"
            " data from different source, for example network or ftp server"))
    data_action = models.CharField(
        _('data action'), blank=True,
        max_length=255,
        help_text=_(
            "What will be done with data, for example,"
            " create or some custom opeartion eg. download image from server"
        )
    )
    filter_dataset = models.BooleanField(
        _('filter custom dataset'), default=True, help_text=_(
            "Check it if you have custom queryset and want to filter"
            " from querystring, for example from admin button"))
    filter_querystring = models.CharField(
        _('querystring'), max_length=255, blank=True, help_text=_(
            "Querystring from admin or other source, if you choose import"
            " action this params will be used for updating!"))

    language = models.CharField(
        _('language'), blank=True,
        max_length=255, choices=django_settings.LANGUAGES, help_text=_(
            "Activates language before action, for example if you want you"
            " have modeltranslation app and you need to export or import only"
            " for choosed language"))
    hide_translation_fields = models.BooleanField(
        _('Hide translation prefixed fields'),
        default=True, help_text=_(
            "If you don't want to create _lang field"
            " settings and dublicate in attribute list, handy if you using"
            " modeltranslation"))

    create_fields = models.BooleanField(
        _('Create settings for fields'), default=True,
        help_text=_("Automaticaly creates all settings for model fields"))
    populate_from_file = models.BooleanField(
        _('Populate settings from file'), default=False,
        help_text=_(
            "Read start row, end row and first worksheet page"
            " from given file"))
    include_related = models.BooleanField(
        _('Include related fields'), default=True, help_text=_(
            "Include ForeignKey and ManyToManyField fields when using "
            "'create fields' option"))
    edit_attributes = models.BooleanField(
        _('Edit field attributes'), default=False, help_text=_(
            "If you want to add custom attributes for custom action, by"
            " checking this option, you can edit attributes"))

    def fields_with_converters(self):
        """Return iterator of fields with converters"""

        from .lib.manager import manager

        fields = self.fields.exclude(skip=True)
        for field in fields:
            field.ordered_converters = []
            if field.converters:
                for converter in field.converters.split(','):
                    field.ordered_converters.append(
                        manager.get('converter', converter))

            yield field

    def populate_from_buffer_file(self):
        # TODO: move set dimensions in processor open, create methods

        from .lib.manager import manager

        processor = manager.make_processor(self, from_extension=True)
        max_row, max_col = processor.open(self.buffer_file.path)
        processor.set_dimensions(0, 0, max_row, max_col)

        start_row = 0

        index = 1
        while index < max_row:
            row = processor.read(index - 1)
            start_row = index

            for col_index, col in enumerate(row):
                if col:
                    index = max_row
                    break
            index += 1

        self.start_row = start_row
        self.end_row = max_row

    def create_default_fields(self, exclude=None, add_label=True):
        """Create all fields for selected model"""

        fields = []

        if not exclude:
            exclude = []

        if not self.model:
            return []

        for name, label in model_attributes(self):
            label = label if self.action != self.IMPORT and add_label else ''
            if name not in exclude:
                if '|_m_|' in name:
                    converters = 'comalist'
                else:
                    converters = 'string'

                field = self.fields.create(
                    attribute=name, name=label, converters=converters)
                fields.append(field)

        return fields

    def run(self):
        """Run import or export task from celery"""

        from .lib.manager import manager

        # TODO: move to tasks

        if 'django_rq' in django_settings.INSTALLED_APPS \
                and SETTINGS['BROKER'] == 'rq':
            from .tasks import export_data, import_data

            if self.action == self.EXPORT:
                export_data.delay({'id': self.id})
            elif self.action == self.IMPORT:
                import_data.delay({'id': self.id})
        elif 'celery' in django_settings.INSTALLED_APPS \
                and SETTINGS['BROKER'] == 'celery':
            from .tasks import export_data, import_data

            if self.action == self.EXPORT:
                export_data.apply_async(args=[{'id': self.id}])
            elif self.action == self.IMPORT:
                import_data.apply_async(args=[{'id': self.id}])
        else:
            if self.action == self.EXPORT:
                manager.export_data(self)
            elif self.action == self.IMPORT:
                manager.import_data(self)

    class Meta:
        verbose_name = _('settings')
        verbose_name_plural = _('settings')

        ordering = ('-id',)

    def __str__(self):
        return self.name or self.worksheet or str(self.id)


@receiver(post_save, sender=Settings)
def settings_post_save(sender, **kwargs):
    settings = kwargs['instance']

    post_save.disconnect(settings_post_save, sender=Settings)

    if settings.create_fields:
        settings.create_default_fields()
        settings.create_fields = False

    if settings.action == settings.IMPORT \
            and settings.buffer_file and settings.populate_from_file:
        settings.populate_from_buffer_file()
        settings.populate_from_file = False

    settings.save()

    post_save.connect(settings_post_save, sender=Settings)


@python_2_unicode_compatible
class Sequence(models.Model):
    name = models.CharField(_('name'), max_length=255)
    buffer_file = models.FileField(
        _('file'), upload_to=SETTINGS['path'], db_index=True, blank=True)

    settings = models.ManyToManyField(
        Settings, verbose_name=_('settings'), related_name='sequences')

    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('sequence')
        verbose_name_plural = _('sequences')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Field(PositionRelatedMixin):

    """Data mapping field for Settings"""

    POSITION_RELATED_FIELD = 'settings'

    # TODO: more filters and translations

    FILTER_CHOICES = (
        ('icontains', 'icontains'),
        ('contains', 'contains'),
        ('iexact', 'iexact'),
        ('exact', 'exact'),
        ('in', 'in'),
        ('gt', 'gt'),
        ('gte', 'gte'),
        ('lt', 'lt'),
        ('lte', 'lte'),
        ('not', 'not')
    )

    name = models.CharField(_('name'), max_length=255, blank=True)
    attribute = models.CharField(
        _('model attribute'), max_length=255)
    skip = models.BooleanField(_('skip'), default=False)

    update = models.BooleanField(_('update'), default=True)
    find = models.BooleanField(_('find'), default=False)

    set_filter = models.CharField(
        _('set filter type'), max_length=255, blank=True,
        choices=(
            ('not', _('Not create or update instance if empty cell'),),
        ))
    set_value = models.CharField(
        _('set value'), max_length=255, blank=True)

    find_filter = models.CharField(
        _('find filter type'), max_length=255, blank=True,
        choices=FILTER_CHOICES, default='exact')
    find_value = models.CharField(
        _('find value'), max_length=255, blank=True)

    converters = models.CharField(
        _('converters'), max_length=255, blank=True)

    settings = models.ForeignKey(
        Settings, verbose_name=_('settings'), related_name='fields')

    class Meta(PositionRelatedMixin.Meta):
        verbose_name = _('field')
        verbose_name_plural = _('fields')

    def __str__(self):
        return self.name or self.attribute


@python_2_unicode_compatible
class Context(models.Model):

    """Context for importing values in action"""

    name = models.CharField(_('name'), max_length=255)
    cell = models.CharField(_('cell'), max_length=1000, blank=True)
    value = models.CharField(_('value'), max_length=1000, blank=True)

    settings = models.ForeignKey(
        Settings, verbose_name=_('settings'),
        related_name='contexts', null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('context')
        verbose_name_plural = _('contexts')


@python_2_unicode_compatible
class Report(ActionsMixin):

    """Reports for imported and exported operations and link to files"""

    ERROR = 0
    RUNNING = 1
    SUCCESS = 2

    STATUS_CHOICES = (
        (ERROR, _('Error')),
        (RUNNING, _('Running')),
        (SUCCESS, _('Success'))
    )

    buffer_file = models.FileField(
        _('file'), upload_to=SETTINGS['path'], db_index=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _('status'), choices=STATUS_CHOICES, default=RUNNING)

    started_at = models.DateTimeField(
        _('started at'), auto_now_add=True)
    completed_at = models.DateTimeField(
        _('completed at'), null=True, blank=True)
    updated_at = models.DateTimeField(
        _('updated at'), auto_now=True)

    settings = models.ForeignKey(
        Settings, verbose_name=_('settings'),
        related_name='reports', null=True, blank=True
    )

    objects = models.Manager()
    export_objects = ExportManager()
    import_objects = ImportManager()
    running_objects = RunningManager()

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

        ordering = ('-id',)

    def __str__(self):
        return '{} - {}'.format(self.started_at, self.get_status_display())

    def get_absolute_url(self):
        if self.buffer_file:
            return self.buffer_file.url


@receiver(export_started)
def create_export_report(sender, **kwargs):
    return Report.export_objects.create(
        action=Report.EXPORT, settings=sender.settings)


@receiver(export_completed)
def save_export_report(sender, **kwargs):
    report = sender.report

    report.completed_at = kwargs['date']
    report.buffer_file = kwargs['path']
    report.status = report.SUCCESS
    report.save()

    return report


@receiver(import_started)
def create_import_report(sender, **kwargs):
    return Report.import_objects.create(
        buffer_file=strip_media_root(kwargs['path']),
        settings=sender.settings,
        action=Report.IMPORT)


@receiver(import_completed)
def save_import_report(sender, **kwargs):
    report = sender.report

    report.completed_at = kwargs['date']
    report.save()

    return report


@python_2_unicode_compatible
class Message(PositionRelatedMixin, ErrorChoicesMixin):

    """Report errors with info about step where raised"""

    POSITION_RELATED_FIELD = 'report'

    ERROR = 0
    INFO = 1

    MESSAGE_CHOICES = (
        (ERROR, _('Error')),
        (INFO, _('Info'))
    )

    report = models.ForeignKey(Report, related_name='messages')

    message = models.TextField(_('message'), max_length=10000)
    step = models.PositiveSmallIntegerField(
        _('step'), choices=ErrorChoicesMixin.STEP_CHOICES,
        default=ErrorChoicesMixin.UNDEFINED)
    input_position = models.CharField(
        _('input position'), max_length=10, blank=True)
    input_value = models.TextField(
        _('input value'), max_length=60000, null=True, blank=True)

    type = models.PositiveSmallIntegerField(
        _('type'), choices=MESSAGE_CHOICES, default=ERROR)

    class Meta(PositionRelatedMixin.Meta):
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return self.message


@receiver(error_raised)
def create_error(sender, **kwargs):
    position = kwargs.get('position', '')
    value = kwargs.get('value', None)

    Message.objects.create(
        report=sender.report, message=kwargs['error'],
        step=kwargs['step'], input_position=position,
        input_value=repr(value) if value else None)
