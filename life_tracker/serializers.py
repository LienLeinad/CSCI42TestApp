from rest_framework import serializers

from .models import LifeTracker


class LifeTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = LifeTracker
