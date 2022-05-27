from django import forms
from .models import Quiz, Question, Answer, Profile, LearningSpace, Subject
from django.contrib.auth.models import User
from django.contrib import admin


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'desc', 'number_of_questions', 'time')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('content', 'quiz')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class LearningSpaceForm(forms.ModelForm):
    class Meta:
        model = LearningSpace
        fields = ['title', 'description', 'quizzes', 'subjects']

    title = forms.CharField()
    description = forms.TextInput()
    quizzes = forms.ModelMultipleChoiceField(
        queryset=Quiz.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
