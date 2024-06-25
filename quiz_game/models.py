from django.core.validators import RegexValidator
from django.utils import timezone

from django.db import models
from django.utils.timezone import now


# Create your models here.

class JSQuestion(models.Model):
    question = models.CharField(max_length=1024)
    choices = models.JSONField()
    answer = models.IntegerField()
    created_by = models.CharField(max_length=100, default='Adithya')
    created_date = models.DateField(default=now)
    update_by = models.CharField(max_length=100, null=True, blank=True)
    update_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.question


class User_Register(models.Model):
    name = models.CharField(max_length=100)
    e_mail = models.EmailField(unique=True)
    ph_no = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message='Phone number must be 10 digits')]
    )
    quiz_marks = models.JSONField(default=list)
    quiz_attempts = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)  # Use timezone.now without parentheses
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.e_mail

    def append_score(self, score):
        self.quiz_marks.append(score)
        self.quiz_attempts += 1
        self.save()


class admin_model(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=10)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

