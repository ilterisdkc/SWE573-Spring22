from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


# Django models will be developed in this file

class Question(models.Model):
    header = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.header


class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment_text
