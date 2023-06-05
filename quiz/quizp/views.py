import random

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from quizp.models import *


def main(request):
    return render(request,'main.html')

def show_questions(request):
    questions = Question.objects.all()
    points = 0
    return render(request,'allquestions.html', context={'questions':questions, 'points':points})

class QuizView(View):
    def get(self,request,category_id):
        request.session['score'] = 0
        random_idx = random.sample(range(Question.objects.count()),10)
        questions=Question.objects.filter(id__in=random_idx, category_id=category_id)
        return render(request, 'quiz.html',context={'questions':questions})
    def post(self,request,category_id):
        for i in range(1,11):
            question_id = request.POST.get(f"question_id_{i}")
            answer=request.POST.get(f"answer_{i}")
            question = Question.objects.get(id=question_id)

            if question.correct== answer:
                request.session['score'] += 1

        score = request.session['score']
        Result.objects.create(amount=score, category_id=category_id)
        return HttpResponse(score)

