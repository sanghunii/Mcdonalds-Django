from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
import datetime

from .models import Question

# Create your views here.

def index(request):
  latest_question_list = Question.objects.order_by("-pub_date")[:5]
  context = {
    "latest_question_list": latest_question_list,
  }
  return render(request, "polls/index.html", context)

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
  response = "You're looking at the results of question %s."
  return HttpResponse(response % question_id)

def vote(request, question_id):
  return HttpResponse("You're voting on question %s." % question_id)

def postapi(request):
  racoon_text = request.GET.get('text')
  if len(racoon_text) > 200:
    racoon_text = racoon_text[:200]
  print(racoon_text)
  Question.objects.create(
    question_text = racoon_text,
    pub_date = datetime.datetime.now()
  )
  return HttpResponse(len(racoon_text))