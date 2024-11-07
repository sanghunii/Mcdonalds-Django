from django.db import models

# Create your models here.
class Review(models.Model):
    reviewContents = models.TextField()
    userRatings = models.PositiveSmallIntegerField()
    modelRatings = models.PositiveSmallIntegerField(null=True)
    createdAt = models.DateTimeField(auto_now=True)

