from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list" : latest_question_list}
    return render(request, "polls/index.html", context)


@api_view(["POST"])
def post(request):
    content_type = request.META.get("CONTENT_TYPE")
    text = JSONParser().parse(request)["text"] #Does JSONParser convert the body of request instance into dict instance??
    print(text)
    if ((content_type == "application/json") &  (len(text) <= 200)): # Additional condition that checks if the content type is correct
        q = Question.objects.create(question_text=text, pub_date=timezone.now())
        return Response(data = {"id":q.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(data = {"message":"text는 200자를 넘을 수 없습니다. content-type은 JSON형식입니다."}, status=status.HTTP_400_BAD_REQUEST)

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
