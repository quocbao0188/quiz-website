# from .models import Answer
# from django.forms.widgets import RadioSelect
# from django import forms

# # # class QuestionForm(forms.ModelForm):
# # #     answer = forms.ChoiceField(required=True, widget=forms.RadioSelect())

# # #     def __init__(self, data, question=None, *args, **kwargs):
# # #         super(QuestionForm, self).__init__(*args, **kwargs)
# # #         self.fields['answer'].choices = [(a.text, a.value) for a in Answer.objects.filter(question=question)]

# # #     class Meta:
# # #         model = Question
# # #         fields = ['label',]
# # from django import forms
# # from django.forms.widgets import RadioSelect


# class QuestionForm(forms.Form):
#     def __init__(self, question_id, *args, **kwargs):
#         super(QuestionForm, self).__init__(*args, **kwargs)
#         choice_list = [x for x in Answer.objects.filter(question_id=question_id)]
#         self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)