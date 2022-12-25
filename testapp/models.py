from django.db import models


class Question(models.Model):
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    question = models.TextField(blank=False, help_text="поле для ввода вопроса", verbose_name="Вопрос")
    categories = models.ManyToManyField("QuestionCategory", verbose_name="категория")

    data_response = models.JSONField(
        default={"question_category": [], "answer_options": [], "correct_answers": []},
        help_text="для хранения вариантов ответа и верных ответов",
        verbose_name="варианты и ответы",
    )

    def __str__(self):
        return self.question


class QuestionCategory(models.Model):
    title = models.CharField(
        max_length=150,
        blank=False,
        help_text="поле для ввода названий категорий вопросов",
        verbose_name="категория вопроса",
    )
    description = models.CharField(
        max_length=200,
        blank=False,
        help_text="поле для ввода краткого описания категории",
        verbose_name="описание категории вопроса",
    )

    def __str__(self):
        return self.title
