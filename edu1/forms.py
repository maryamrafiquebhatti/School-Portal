from django import forms
from .models import Cohort, Lesson, Question, AssignCohort
from .models import Question, QuestionTrueFalse, QuestionMCQS, QuestionFillInBlank

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CohortForm(forms.ModelForm):
    class Meta:
        model = Cohort
        fields = ['name']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'cohort']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['type', 'statement', 'lesson']
        
class QuestionTrueFalseForm(forms.ModelForm):
    class Meta:
        model = QuestionTrueFalse
        fields = ['answer']

class QuestionMCQSForm(forms.ModelForm):
    class Meta:
        model = QuestionMCQS
        fields = ['option_a', 'option_b', 'option_c', 'option_d', 'answer']

class QuestionFillInBlankForm(forms.ModelForm):
    class Meta:
        model = QuestionFillInBlank
        fields = ['answer']


class AssignCohortForm(forms.ModelForm):
    class Meta:
        model = AssignCohort
        fields = ['user', 'cohort']

from django import forms
from .models import Score

class AttemptQuestionForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['marks']  
