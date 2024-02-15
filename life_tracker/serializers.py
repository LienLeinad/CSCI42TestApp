from rest_framework.serializers import ModelSerializer

from .models import LifeCounter


class LifeCounterSerializer(ModelSerializer):
    class Meta:
        model = LifeCounter
        fields = (
            "p1_life",
            "p2_life",
        )
