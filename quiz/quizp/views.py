import random

from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

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
            return render(request,'result.html', context={'score':score, 'user_results':user_results})
        else:
            score = request.session['score']
            Result.objects.create(amount=score, category_id=category_id)
            user_results = "Register to see your other results"
            return render(request, 'result.html', context={'score': score,'user_results':user_results})
