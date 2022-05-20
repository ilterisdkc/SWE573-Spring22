from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from myapp.models import Question, Comment
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape


# Create your views here.

class QuestionCreateView(CreateView):
    model = Question
    fields = ['header', 'description']
    template_name = 'myapp/templates/question_add.html'
    success_url = '/question/add/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionDataTable(BaseDatatableView):
    model = Question
    columns = ['id', 'header', 'description', 'user', 'create_time']

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(header__istartswith=search)
        return qs

    def datatable_static(request, *args, **kwargs):
        questions = Question.objects.all()
        return render(
            request=request,
            template_name="myaapp/templates/question_datatable.html",
            context={
                "question_list": questions
            })


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['header', 'description']
    template_name = 'myapp/templates/question_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentCreateView(CreateView):
    model = Comment
    fields = ['question', 'comment_text']
    template_name = 'myapp/templates/comment_add.html'
    success_url = '/comment/add'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['comment_text']
