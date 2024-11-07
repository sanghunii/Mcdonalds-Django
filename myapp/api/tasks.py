from myapp.celery import app
import time
from .models import Review

@app.task()
def predict(string:str, review_id:int) -> None:
    modelRatings = len(string)
    time.sleep(10)
    review = Review.objects.get(id = review_id)
    review.modelRatings = modelRatings
    review.save(update_fields=['modelRatings'])