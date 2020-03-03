"""
Management command for generating external ids for users.
"""

import logging

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from openedx.core.djangoapps.external_user_ids.models import ExternalId, GenerateExternalIdsConfig

User = get_user_model()
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):
    """
    Generate ExternalIds for a list of Users IDs in the GenerateExternalIdsConfig
    """
    def _log_results(self, user_id_list, unknown_users, created_id_list, existing_id):
        logger.info('Attempted to create External IDs for the following users: {}'.format(user_id_list))
        logger.info('Could not find the following user IDs: {}'.format(unknown_users))
        logger.info('Created new IDs for the following user IDs: {}'.format(created_id_list))
        logger.info('The following users already had External IDs: {}'.format(existing_id))

    def handle(self, *args, **options):
        try:
            config = GenerateExternalIdsConfig.objects.get()
        except GenerateExternalIdsConfig.DoesNotExist:
            logger.error('A GenerateExternalIdsConfig in the app database is required.')
            return
        user_id_strs = [user_id.strip() for user_id in config.user_list.split(',')]
        user_id_list = []
        for user_id in user_id_strs:
            try:
                user_id_list.append(int(user_id))
            except ValueError:
                logger.info(
                    'User ID [{}] is not an integer and is not considered a user id, it will be ignored.'.format(user_id)
                )

        id_type = config.external_id_type
        created_id_list = []
        existing_id = []

        user_list = User.objects.filter(
            id__in=user_id_list
        )
        for user in user_list:
            new_external_id, created = ExternalId.objects.get_or_create(
                user=user,
                external_id_type=id_type,
            )
            if created:
                created_id_list.append(user.id)
            else:
                existing_id.append(user.id)
        found_user_ids = created_id_list + existing_id
        unknown_users = list(set(user_id_list) - set(found_user_ids))
        self._log_results(user_id_list, unknown_users, created_id_list, existing_id)
