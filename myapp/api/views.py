from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Review
from .tasks import predict

#for REST - API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
# Create your views here.


##serializer
from .serializers import ReviewSerializer

##Celery
from .tasks import predict


from django.core.paginator import Paginator
from math import ceil
    



@api_view(["POST" ,"GET"])
def review(request):
    if request.method == "POST":
        reviewContents = request.data['reviewContents']
        userRatings = request.data['userRatings']
        R = Review.objects.create(reviewContents = reviewContents, userRatings=userRatings)
        review_id = R.id
        predict.delay(reviewContents, review_id)
        return Response({'id':review_id}, status=status.HTTP_201_CREATED)


    elif request.method == "GET":
        allReviews = Review.objects.order_by('id')
        page = int(request.query_params.get('page',1))          ##없으면 1로 설정 
        paginator = Paginator(allReviews, request.query_params.get('size'))          ##한페이지당 5개 보내주기
        reviews = paginator.get_page(page)          ##보낼 페이지 보내주기
        maxPage = max(paginator.page_range)
        result = {'reviews': [{"id": review.id, 
                               "reviewContents":review.reviewContents, 
                               "modelRatings":review.modelRatings} for review in reviews],
                    'pageinfo': maxPage}
        return Response(result, status=status.HTTP_200_OK )










@api_view(["GET"])
def review_id(request, reviewId):
    if request.method == "GET":
        review = Review.objects.filter(id = reviewId)
        if (review) :
            review = review = Review.objects.get(id = reviewId)
            result = {"id": review.id, "reviewContents": review.reviewContents, "modelRatings":review.modelRatings}
            return Response(result, status = status.HTTP_200_OK)
        else :
            result = {
	                "message": "등록되지 않은 메세지 id입니다"
                    }
            return  Response(result, status = status.HTTP_204_NO_CONTENT)
        
@api_view(["GET"])
def check(request, checkId):
    if request.method == "GET":
        review = Review.objects.filter(id = checkId)
        if (review):
            review = Review.objects.get(id = checkId)
            if (review.modelRatings) :
                result = {"status":True}
                return Response(result, status = status.HTTP_200_OK)
                
            else :
                result = {"status":False}
                return  Response(result, status = status.HTTP_200_OK)
        else :
            result = {
	                "message": "등록되지 않은 메세지 id입니다"
                    }
            return  Response(result, status = status.HTTP_204_NO_CONTENT)

""" 여기가 원래 GET 코드 
    elif request.method == "GET":
        page = request.query_params.get('page')
        page = int(page)
        size = request.query_params.get('size')
        size = int(size)
        start_id = (page - 1) * size
        end_id = page * size
        allReviews = Review.objects.all()
        reviews = allReviews[start_id:end_id]
        numOfReviews = len(allReviews)
        maxPage = math.ceil(numOfReviews / size)
        result = {'reviews': [{"id": review.id, 
                               "reviewContents":review.reviewContents, 
                               "modelRatings":review.modelRatings} for review in reviews],
                    'pageinfo': maxPage}
        return Response(result, status = status.HTTP_200_OK)
""" 
    

        
        
        







"""
####reference
@api_view(['GET', 'POST'])
def drf_api(request):
    
    ##들어온 API요청이 GET이라면
    if request.method == 'GET':
        question_id = request.GET.get('question_id')

        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            res = {
                '204_no_content': f"{question_id}에 해당하는 Question이 존재하지 않습니다."
            }
            return Response(res, status=status.HTTP_204_NO_CONTENT)
        
        serializer = QuestionSerializer(question)
        res = {
            'question_text': serializer.data['question_text'],
            'question_text_length': len(serializer.data['question_text']),
        }
        return Response(res, status=200)
    
    
    ##들어온 API요청이 POST라면
    if request.method == 'POST':
        data = request.data     #body의 원시데이터를 가져온다. 
        data['pub_date'] = datetime.datetime.now()
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid(raise_exception=True):   #유효성 검사
            serializer.save()  #DB에 저장.
            return Response(status=status.HTTP_201_CREATED)
"""