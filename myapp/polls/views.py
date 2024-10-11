from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Question
from django.utils import timezone

from .models import Question

#for API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer
from rest_framework import status
import json



def index(request):
    return HttpResponse("안녕안녕?")

def detail(request, question_id):
    return HttpResponse("This quesiton ID is %s" % question_id)

def results(request, question_id):
    response = "안녕안녕 %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("안녕안녕 %s." % question_id)


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




def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_question_list": latest_question_list}

    return render(request, "polls/index.html", context)


##id를 가져오는게 이상한듯
##axios를 이용해서 GET API를 사용했을때 params를 이용해서 id를 보내면 
##쿼리파라미터가 붙음.
@api_view(['GET'])
def get_data(request):
    question_id = request.GET.get('id')
    question_obj = Question.objects.filter(id=question_id)
    if question_obj.exists():
#QuestionSerializer를 사용할때 다수의 qeuryset을 직렬화 할때는 many=True 파라미터 사용해야함.
        serializer = QuestionSerializer(Question.objects.get(id=question_id)) #직렬화하고
        q_text = serializer.data['question_text']
        q_length = len(serializer.data['question_text'])
        data={
            'text': q_text,
            'lenth': q_length
        }
        return Response(data, status=200)
    else:
        #204NOContent에러 발생
        return Response(serializer.error, status=status.HTTP_204_NO_CONTENT)