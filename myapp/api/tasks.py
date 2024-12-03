from myapp.celery import app
import time

from .models import Review

import time 
import random 


@app.task()
def predict(string:str, review_id: int) -> int:
    time.sleep(15)
    modelRatings = random.randint(1,5)
    review = Review.objects.get(id=review_id)
    review.modelRatings = modelRatings
    review.save()
    
    return modelRatings