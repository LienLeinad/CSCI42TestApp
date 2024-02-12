from django.db import models


class LifeCounter(models.Model):
    p1_life = models.IntegerField(default=40)
    p2_life = models.IntegerField(default=40)
