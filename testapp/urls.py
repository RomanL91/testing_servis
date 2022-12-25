from django.urls import path

from testapp import views as testapp_view

urlpatterns = [
    path("", testapp_view.Home.as_view(), name="main_page"),
    path("testing/<int:pk>/", testapp_view.TestView.as_view(), name="testing"),
    path("testing_q/<int:pk>/", testapp_view.QuestionFormView.as_view(), name="testing_q"),
]
