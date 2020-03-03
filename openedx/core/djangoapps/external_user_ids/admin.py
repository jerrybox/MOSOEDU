from django.contrib import admin
from .models import GenerateExternalIdsConfig


@admin.register(GenerateExternalIdsConfig)
class GenerateExternalIdsConfigAdmin(admin.ModelAdmin):
    """
    Admin config for the Generation External IDs Configuration Model
    """
    list_display = ('user_list', 'external_id_type')
