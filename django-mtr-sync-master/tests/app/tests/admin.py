from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from mtr.utils.helpers import themed_path


class AdminMixinTest(TestCase):

    def setUp(self):
        self.password = 'admin_password'
        self.user = User.objects.create_superuser(
            'admin', 'admin', password=self.password)
        self.client.login(username=self.user.username, password=self.password)

    def test_mixin_has_buttons_in_change_view(self):
        content = self.client.get(reverse(
            'admin:app_person_changelist'))

        self.assertIn(
            themed_path('mtr/sync/admin/change_list.html', True),
            [template.name for template in content.templates])

        self.assertContains(content, 'Export')
        self.assertContains(content, 'Import')

    def test_settings_export_import_modified_by_link(self):
        link = reverse('admin:mtr_sync_settings_add')

        content = self.client.get(
            '{}?action=export&model=app.person&filter='
            'security_level__gte%3D10%26surname__icont'
            'ains%3Ddas%26o%3D-3.2%26gender__exact%3DM'
            '%26fields=action_checkbox%2Cname%2Csurname%'
            '2Csecurity_level%2Cgender'.format(link))
        form = content.context['adminform'].form

        self.assertEqual(form.initial['action'], 0)
        self.assertEqual(form.initial['model'], 'app.person')
        self.assertEqual(form.initial['create_fields'], True)
        self.assertEqual(
            form.initial['filter_querystring'],
            'security_level__gte=10&surname__icontains=das'
            '&o=-3.2&gender__exact=M&fields=action_check'
            'box,name,surname,security_level,gender')

        content = self.client.get(
            '{}?action=import&model=app.person'.format(link))
        form = content.context['adminform'].form

        self.assertEqual(form.initial['action'], 1)
        self.assertEqual(form.initial['model'], 'app.person')
        self.assertEqual(form.initial['create_fields'], True)
        self.assertEqual(form.initial['populate_from_file'], True)
