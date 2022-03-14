from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from myapp.models import Question, Comment


# Create your views here.

class QuestionCreateView(CreateView):
    model = Question
    fields = ['header', 'description']
    template_name = 'myapp/templates/question_add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['header', 'description']


class CommentCreateView(CreateView):
    model = Comment
    fields = ['comment_text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['comment_text']
