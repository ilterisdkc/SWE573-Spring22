from django.urls import path
from myapp.views import QuestionCreateView, QuestionUpdateView, CommentCreateView, CommentUpdateView, QuestionDataTable

urlpatterns = [
    path('question/add', QuestionCreateView.as_view(), name='question-add'),
    path('question/<int:pk>', QuestionUpdateView.as_view(), name='question-update'),
    path('comment/add', CommentCreateView.as_view(), name='comment-add'),
    path('comment/<int:pk>', CommentUpdateView.as_view(), name='comment-update'),
    path('questions', QuestionDataTable.as_view(), name='question-list'),
]