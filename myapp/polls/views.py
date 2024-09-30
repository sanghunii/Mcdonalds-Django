from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list" : latest_question_list}
    return render(request, "polls/index.html", context)

def get(request):
    message = request.GET.get('abc')
    print(message)
    return HttpResponse(len(message))

def detail(request, question_id):
    return HttpResponse("너굴너굴너굴맨 %s번 질문입니다."%question_id)

def results(request, question_id):
    response = "너굴너굴너굴맨 %s번 답변에 투표하셨습니다."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("너굴너굴너굴맨 %s번 투표 결과입니다." %question_id)
