from django.contrib import admin
from myapp.models import Question
from myapp.models import Comment

# Register your models here.
admin.site.register(Question)
admin.site.register(Comment)
