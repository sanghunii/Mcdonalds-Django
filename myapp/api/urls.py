from django.urls import path

from . import views

urlpatterns = [
    path("review", views.review, name="review"),
    path("review/<int:reviewId>", views.review_id, name = "review_id"),
    path("check/<int:checkId>", views.check, name = "check")
]