from django.db import models
from django.contrib.auth.models import User
import random
from PIL import Image
from ckeditor.fields import RichTextField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(max_length=1000)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img_ = Image.open(self.avatar.path)
        img = img_.convert('RGB')
        img.seek(0)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    number_of_questions = models.IntegerField(default=1)
    time = models.IntegerField(help_text="Duration of the quiz in seconds", default="1")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()


class Question(models.Model):
    content = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"


class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)


class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField(max_length=2000, blank=True)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    contributors = models.ManyToManyField(Contributor, blank=True)
    fileinput = models.FileField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return str(self.title)


class LearningSpace(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    coLearners = models.ManyToManyField(Contributor, blank=True)
    quizzes = models.ManyToManyField(Quiz, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return str(self.title)
