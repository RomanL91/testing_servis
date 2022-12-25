from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import Question, QuestionCategory

admin.site.register(QuestionCategory)


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    list_display = ("question", "data_response")
    list_filter = ("categories",)
