"""
Test the Generate External Ids Management command.
"""
import mock

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from student.tests.factories import UserFactory

from openedx.core.djangolib.testing.utils import skip_unless_lms

# external_ids is not in CMS' INSTALLED_APPS so these imports will error during test collection
if settings.ROOT_URLCONF == 'lms.urls':
    from openedx.core.djangoapps.external_user_ids.models import (
        ExternalId,
        GenerateExternalIdsConfig
    )
    from openedx.core.djangoapps.external_user_ids.tests.factories import ExternalIDTypeFactory


@skip_unless_lms
class TestGenerateExternalIds(TestCase):
    """
    Test generating ExternalIDs for Users.
    """
    def setUp(self):
        self.users = UserFactory.create_batch(10)
        self.user_id_list = [str(user.id) for user in self.users]

    def test_generate_ids_for_all_users(self):
        GenerateExternalIdsConfig.objects.create(
            user_list=','.join(self.user_id_list),
            external_id_type=ExternalIDTypeFactory.create(),
        )

        assert ExternalId.objects.count() == 0
        call_command('generate_external_ids')
        assert ExternalId.objects.count() == 10

    def test_no_new_for_existing_users(self):
        id_type = ExternalIDTypeFactory.create()
        GenerateExternalIdsConfig.objects.create(
            user_list=','.join(self.user_id_list),
            external_id_type=id_type,
        )

        for user in self.users:
            ExternalId.objects.create(
                user=user,
                external_id_type=id_type
            )

        assert ExternalId.objects.count() == 10
        call_command('generate_external_ids')
        assert ExternalId.objects.count() == 10

    def test_bad_input_does_not_break(self):
        user_id_list_bad = self.user_id_list + ['abc', ' ', '\n']
        GenerateExternalIdsConfig.objects.create(
            user_list=','.join(user_id_list_bad),
            external_id_type=ExternalIDTypeFactory.create(),
        )

        assert ExternalId.objects.count() == 0
        call_command('generate_external_ids')
        assert ExternalId.objects.count() == 10

    @mock.patch('openedx.core.djangoapps.external_user_ids.management.commands.generate_external_ids.logger')
    def test_no_config(self, mock_logger):
        assert ExternalId.objects.count() == 0
        call_command('generate_external_ids')
        mock_logger.error.assert_called_with('A GenerateExternalIdsConfig in the app database is required.')
        assert ExternalId.objects.count() == 0
