from django.shortcuts import render
from quizp.models import *


def main(request):
    return render(request,'main.html')

def show_questions(request):
    questions = Question.objects.all()
    return render(request,'allquestions.html', context={'questions':questions})