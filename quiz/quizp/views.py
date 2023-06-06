import base64
import io
import random

from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

import numpy as np
import matplotlib.pyplot as plt

from quizp.models import *
from quizp.forms import *

def main(request):
    return render(request,'main.html')

def show_questions(request):
    questions = Question.objects.all()
    points = 0
    return render(request,'allquestions.html', context={'questions':questions, 'points':points})

class RegisterUserView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'register_user.html', context={'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            User.objects.create(username=data.get('username'), password=data.get('password'),
                                first_name=data.get('first_name'), last_name=data.get('last_name'),
                                email=data.get('email'))

            msg = 'użytkownik zarejestrowany pomyslnie!'
            return render(request, 'main.html', {'msg': msg})
        else:
            return render(request, 'register_user.html', context={'form': form})
class LoginView(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'login.html',context={'form':form})

    def post(self, request):
        form = LoginUserForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = User.objects.get(username=username, password=password)
            login(request, user)
            msg = f"zalogowano użytkownika {user}"
            return render(request, 'main.html', {'msg': msg})
        else:
            msg = 'bledne dane'
            return render(request, 'login.html', context={'form': form, 'msg': msg})

class LogoutView(View):
    def get(self, request):
        logout(request)
        msg = "wylogowano użytkownika"
        return render(request, 'main.html', {'msg': msg})

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


        if request.user.is_authenticated:
            score = request.session['score']
            Result.objects.create(amount=score, category_id=category_id, user_id=request.user.id)
            user_results=Result.objects.filter(user_id=request.user.id)
            y_points = []
            for results in user_results:y_points.append(results.amount)
            plt.title('Your results on plot')
            plt.ylabel('Points')
            plt.xlabel('attempts')
            plt.plot(y_points,marker='o')
            plt.ylim(1,11)
            plt.yticks(range(1,12),[str(i) if i <=10 else '' for i in range(1,12)])
            plt.xticks(range(len(y_points)), [str(i) for i in range(1, len(y_points)+1)])
            buffer = io.BytesIO()
            plt.savefig(buffer,format='png')
            buffer.seek(0)
            image_png=buffer.getvalue()
            buffer.close()
            graphic=base64.b64encode(image_png)
            graphic=graphic.decode('utf-8')

            users_results=Result.objects.all()
            hist_data = []
            for results in users_results: hist_data.append(results.amount)
            plt.clf()
            plt.title('Users results')
            plt.ylabel('attempts')
            plt.xlabel('Points')
            plt.hist(hist_data)
            buffer=io.BytesIO()
            plt.savefig(buffer,format='png')
            buffer.seek(0)
            image_png=buffer.getvalue()
            buffer.close()
            graphic_hist=base64.b64encode(image_png)
            graphic_hist=graphic_hist.decode('utf-8')
            return render(request,'result.html', context={'score':score, 'user_results':user_results, 'plot':graphic, 'hist':graphic_hist})
        else:
            score = request.session['score']
            Result.objects.create(amount=score, category_id=category_id)
            user_results = None
            return render(request, 'result.html', context={'score': score,'user_results':user_results})
