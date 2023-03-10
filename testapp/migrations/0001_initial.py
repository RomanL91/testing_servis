# Generated by Django 4.1.4 on 2022-12-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="QuestionCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "title",
                    models.CharField(
                        help_text="поле для ввода названий категорий вопросов",
                        max_length=150,
                        verbose_name="категория вопроса",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="поле для ввода краткого описания категории",
                        max_length=200,
                        verbose_name="описание категории вопроса",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.TextField(help_text="поле для ввода вопроса", verbose_name="Вопрос")),
                (
                    "data_response",
                    models.JSONField(
                        default={"answer_options": [], "correct_answers": [], "question_category": []},
                        help_text="для хранения вариантов ответа и верных ответов",
                        verbose_name="варианты и ответы",
                    ),
                ),
                ("categories", models.ManyToManyField(to="testapp.questioncategory", verbose_name="категория")),
            ],
        ),
    ]
