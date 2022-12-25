from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserRegisterForm
from .models import Profile as PR


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Ваш аккаунт создан: можно войти на сайт.")
            return redirect("authapp:login")
    else:
        form = UserRegisterForm()
    return render(request, "authapp/register.html", {"form": form})


@login_required()
def profile(request):
    # получаю информацию по тестам определенного пользователя
    user_test_information = PR.objects.filter(user_id=request.user.pk)
    # собираю контекст для передачи в шаблон
    # где ключ data, а значения словаль в котором ключи - это ключ сессии
    # значения - информация о тесте(номера вопросов, правильность ответов, и т.д.)
    context = dict(data={f'{el.test_information["session_key"]}': el.test_information for el in user_test_information})
    return render(request, "authapp/profile.html", context=context)
