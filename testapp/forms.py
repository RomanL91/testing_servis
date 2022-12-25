from django import forms

from .models import Question


class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        question = Question.objects.filter(pk=kwargs["initial"]["kwargs"]["pk"])

        self.fields["answer options"] = forms.MultipleChoiceField(
            error_messages={"required": "Выберите один или несколько ответов и нажмите кнопку ОК"},
            label="Варианты ответов",
            # help_text='Выберите один или несколько ответов и нажмите кнопку ОК',
            widget=forms.CheckboxSelectMultiple,
            choices=[(answer_options, answer_options) for answer_options in question[0].data_response["answer_options"]]
            # choices=[(i, i) for i in Question.objects.get(pk=pk).data_response['answer_options']]
        )
