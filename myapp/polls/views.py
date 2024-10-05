from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Question
from django.utils import timezone

from .models import Question

def index(request):
    return HttpResponse("안녕안녕?")

def detail(request, question_id):
    return HttpResponse("안녕 %s 안녕? ." % question_id)

def results(request, question_id):
    response = "안녕안녕 %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("안녕안녕 %s." % question_id)

def string_length(request):
    #여기서 해야할 일
    # 1. 받아온거 글자 길이 200넘는지 확인 (넘으면 200으로 짤라)
    # 2. 글자 길이 확인해서 담아서 보내기 
    message = request.GET.get('abc')

    if (len(message) > 200):
        message = message[:200]
    
    print(message)

    Question.objects.create(
        question_text = message,
        pub_date = timezone.now()
    )


    return HttpResponse(len(message))

"""
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    output = " ".join([q.question_text for q in latest_question_list])

    return HttpResponse(template.render(context, request))
"""

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_question_list": latest_question_list}

    return render(request, "polls/index.html", context)