"""ilteris_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import QuestionCreateView, CommentCreateView, QuestionUpdateView, CommentUpdateView, QuestionDataTable

urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/add/', QuestionCreateView.as_view(), name='question-add'),
    path('question/<int:pk>', QuestionUpdateView.as_view(), name='question-update'),
    path('comment/add', CommentCreateView.as_view(), name='comment-add'),
    path('comment/<int:pk>', CommentUpdateView.as_view(), name='comment-update'),
    path('questions', QuestionDataTable.as_view(), name='question-list'),
]
