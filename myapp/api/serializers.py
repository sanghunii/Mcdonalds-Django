from .models import Review
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        class Meta:
            model = Review
            """
            fields = (
                'id',
                'reviewContents',
                'modelRatings',
            ) #Review모델 객체의 해당 field들에 대해서만 직렬화를 시도한다. 
            """
            exclude = ("userRatings", "createdAt",)



class TestSerializer(serializers.ModelSerializer):
    class Meta:
        class Meta:
            model = Review
            exclude = ("userRatings", "createdAt",)