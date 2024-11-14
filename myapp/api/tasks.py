from myapp.celery import app
import time

from .models import Review



@app.task()
def predict(string:str, review_id: int):
    modelRatings = len(string)
    time.sleep(60)

    review = Review.objects.get(id=review_id)
    review.modelRatings = modelRatings
    review.save()
    
    return modelRatings