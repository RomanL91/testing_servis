from random import choices

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView

from authapp.models import Profile as PR

from .forms import QuestionForm
from .models import Question, QuestionCategory


class Home(ListView):
    queryset = QuestionCategory.objects.all()
    template_name = "testapp/home.html"
    context_object_name = "categorys"


class TestView(DetailView):
    model = QuestionCategory

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # извлекаем все вопросы категории
        category_questions = Question.objects.filter(categories__title=self.object)
        # отбираем 10 случайный вопросов
        questions_for_testing = set(choices(category_questions, k=10))
        # готовим данные для BD->Profile.test_information
        # ставим флаг 'unanswered' для выбранных вопросов(questions_for_testing)
        test_information = {f"{i.pk}": "unanswered" for i in questions_for_testing}
        # помечаем какой категории тест
        test_information.setdefault("cat_test", self.object.__str__())
        user = request.user
        print(user)
        # создаем новую сессию для этого теста
        request.session.create()
        # получаем ключ новой сессии
        sessions_key = request.session.session_key
        # готовим данные для BD->Profile.test_information
        test_information.setdefault("session_key", sessions_key)
        # создаю профиль теста с указанием кто создал и подготовленной информацией выше
        test_profile = PR(user=user, test_information=test_information)
        test_profile.save()
        # перенаправляю пользователя на страницу с первым вопросом
        # по сути это представление как промежуточный этап, так как оно само по себе
        # не выводит ничего, только перенаправляет
        return HttpResponseRedirect(reverse("testapp:testing_q", kwargs={"pk": category_questions[0].pk}))


class QuestionFormView(FormView):
    form_class = QuestionForm
    template_name = "testapp/question_detail.html"

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.__dict__

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            # добавляю контекст для шаблона от конкретного вопроса,
            # который будет представлен пользователю
            kwargs["question"] = Question.objects.filter(pk=self.kwargs["pk"])[0]
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # достаю контекс вопроса, который используется в этом предсавлении
        question_object = self.get_context_data()
        # достаю правильный/ые ответ/ты
        correct_answers = question_object["question"].data_response["correct_answers"]
        # выбранные пользователем ответы
        # выбранный ответ из формы
        # =================================================================
        from django.contrib import messages

        try:
            select_answer = dict(form.data)["answer options"]
        except:
            messages.success(request, f"Выберите один или несколько ответов и нажмите кнопку ОК")
            return self.form_invalid(form)
        # =============================================================================
        # нахожу сессию теста по ключу в Profile используя клююч этой сессии
        test_session = PR.objects.filter(test_information__session_key=request.session.session_key)[0]
        # сравниваю ответы пользователя и правильные ответы
        if select_answer == correct_answers:
            # изменяю статус вопроса в профиле для этой сессии теста если ответ полностью совпадает
            test_session.test_information.update({str(kwargs["pk"]): "correctly"})
        else:
            test_session.test_information.update({str(kwargs["pk"]): "incorrectly"})
        test_session.save()
        # =============================================================================
        correct_answers_given = 0
        wrong_answers_given = 0
        all_test_questions = 0
        if form.is_valid():
            for k, v in test_session.test_information.items():
                if v == "unanswered":
                    return HttpResponseRedirect(reverse("testapp:testing_q", kwargs={"pk": k}))
                elif v == "correctly":
                    correct_answers_given += 1
                    all_test_questions += 1
                elif v == "incorrectly":
                    wrong_answers_given += 1
                    all_test_questions += 1
            else:
                percentage_correct_answers = int((correct_answers_given / all_test_questions) * 100)
            # =========================================================
            from django.shortcuts import render

            context = {
                "cat_test": test_session.test_information["cat_test"],
                "all_test_questions": all_test_questions,
                "correct_answers_given": correct_answers_given,
                "wrong_answers_given": wrong_answers_given,
                "percentage_correct_answers": percentage_correct_answers,
            }
            test_session.test_information.update(context)
            test_session.save()
            return render(request, "testapp/result.html", context=context)
        else:
            return self.form_invalid(form)
