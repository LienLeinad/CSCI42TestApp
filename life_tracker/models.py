from django.db import models


# Create your models here.
class LifeTracker(models.Model):
    p1_name = models.CharField(max_length=255, blank=True, null=True)
    p2_name = models.CharField(max_length=255, blank=True, null=True)
    p1_life = models.IntegerField(default=40)
    p2_life = models.IntegerField(default=40)
