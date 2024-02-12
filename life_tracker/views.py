from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

STARTING_LIFE_TOTAL = 40


class LifeTrackerView(APIView):
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


def index(request):
    return render(request, "index.html")
