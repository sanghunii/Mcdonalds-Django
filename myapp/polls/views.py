from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils import timezone

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list" : latest_question_list}
    return render(request, "polls/index.html", context)

def get(request):
    message = request.GET.get('abc')
    print(message)
    if(len(message) > 200):
        message_cut = message[:200]
        Question.objects.create(question_text=message_cut, pub_date=timezone.now())
    else:
        Question.objects.create(question_text=message, pub_date=timezone.now())
    return HttpResponse(len(message))

def detail(request, question_id):
    return HttpResponse("너굴너굴너굴맨 %s번 질문입니다."%question_id)

def results(request, question_id):
    response = "너굴너굴너굴맨 %s번 답변에 투표하셨습니다."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("너굴너굴너굴맨 %s번 투표 결과입니다." %question_id)
