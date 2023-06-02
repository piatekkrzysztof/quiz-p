from django.db import models
from django.contrib.auth.models import User

class Question_category(models.Model):
    name = models.CharField()

class Question(models.Model):
    category = models.ForeignKey(Question_category, on_delete=models.CASCADE)
    contents = models.CharField(max_length=255)
    ans_A = models.CharField()
    ans_B = models.CharField()
    ans_C = models.CharField()
    ans_D = models.CharField()
    correct = models.CharField()

class Result(models.Model):
    category=models.ForeignKey(Question_category, on_delete=models.CASCADE)
    amount=models.IntegerField()
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

