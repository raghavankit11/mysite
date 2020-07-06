from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Question, Choice


from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class DateInput(forms.DateInput):
#     input_type = 'date'
#
#
class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

