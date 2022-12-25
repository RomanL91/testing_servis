from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import Profile

fields_for_dislplay_and_filter = ("user", "test_information")


@admin.register(Profile)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    list_display = fields_for_dislplay_and_filter
    list_filter = fields_for_dislplay_and_filter
