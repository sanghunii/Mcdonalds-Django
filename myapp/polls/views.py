from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime



from .models import Question


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list":latest_question_list}
    return render(request,"polls/index.html", context)

def detail(request, question_id):
    return HttpResponse("You are looking at question %s."% question_id)

def results(request, question_id):
    response = "You are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You are voting on qeustion %s."% question_id)

def get(request):
    message = request.GET.get('abc')
    print(message)
    Question.objects.create(question_text=message, pub_date=datetime.now())
    return HttpResponse(len(message))


