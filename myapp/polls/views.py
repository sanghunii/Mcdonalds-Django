from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Question
from django.utils import timezone

from .models import Question

#for REST - API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer
from rest_framework import status
import json


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_question_list": latest_question_list}

    return render(request, "polls/index.html", context)

def detail(request, question_id):
    return HttpResponse("This quesiton ID is %s" % question_id)

def results(request, question_id):
    response = "안녕안녕 %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("안녕안녕 %s." % question_id)


##여기가 django-react부분 view 
def string_length(request):
    #여기서 해야할 일
    # 1. 받아온거 글자 길이 200넘는지 확인 (넘으면 200으로 짤라)
    # 2. 글자 길이 확인해서 담아서 보내기 
    message = request.GET.get('abc') #이거 query_parameter받는거임.
                                    #-> axios에서는 params이용해서 query parameter만들고 fetch()이용할때는 직접 url뒤에 query_params추가해줘야 한다.


#request.GET은 HTTP get 메서드로 받은 요청을 받는다. 요청을 받아서 dictionary형태로 변환한다.
#get()은 dictionary메서드임. 즉 request.GET에서 받은 요청을 dictionary형태로 변환하고 .get(key)에서 key에 해당하는 value를 찾는다. 만약 없으면 None반환 이때 에러발생 X
#.get()에서 key에 해당하는 value가 없을경우 에러가 아닌 None을 반환한다. 예외처리를 해줘야할듯? 
#None을 반환했을때 의도적으로 에러를 발생시키고 정보가 제대로 전달되지 않았음을 보여야함.
#근데 막상 해보니깐 None을 반환했을때도 에러(500)가 발생. 왜지 .. ? 

    if (len(message) > 200):
        message = message[:200]
    #if (message == None):          
    #    message = "None"
    print(message)

    Question.objects.create(
        question_text = message,
        pub_date = timezone.now()
    )


    return HttpResponse(len(message))








##axios를 이용해서 GET API를 사용했을때 params를 이용해서 id를 보내면 
##쿼리파라미터가 붙음.
##10월 13일 (일) - GET API요청을 보낼때, 요구한 id에 맞는 contents가 없으면 204 - No Contents 신호를 보내야 하는데 계속 500 server error가 뜬다.
@api_view(['GET'])
def get_data(request):
    question_id = request.GET.get('id')
#.filter(조건) method는 조건에 해당하는 항목이 있으면 해당 데이터를 QuerySet형태로 반환, 없으면 빈 QuerySet을 반환
    question_obj = Question.objects.filter(id=question_id)
    if question_obj.exists():

#QuestionSerializer를 사용할때 다수의 qeuryset을 직렬화 할때는 many=True 파라미터 사용해야함.
#즉 primary key가 아닌 겹칠 수 있는 다른 값을 이용해서 DB를 조회할때는  .get()을 이용해야 할듯
##get은 filter와 다르게 상황에 따라 여러 exception을 발생시킨다.
#1. 조회하려는 데이터가 없을때 => DoesNotExist
#2. 조회하려는 데이터가 여러개일 때 => MultipleObjectsReturned
        serializer = QuestionSerializer(Question.objects.get(id=question_id)) #serializing
        q_text = serializer.data['question_text']
        q_length = len(serializer.data['question_text'])
        res={
            'text': q_text,
            'length': q_length
        }
        return Response(res, status=200)
    else:
        res={
            '204_no_content': f"there is no content corresponding to {question_id}"
        }
        return Response(status=status.HTTP_204_NO_CONTENT)