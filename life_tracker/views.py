from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from .models import LifeCounter
from .serializers import LifeCounterSerializer

# Create your views here.


## REST API
class LifeTrackerViewSet(ModelViewSet):
    queryset = LifeCounter.objects.all()  # There really should only be one
    serializer_class = LifeCounterSerializer

    def list(self, request: Request, pk=None):
        created = False
        # Check if a life counter exists
        if not LifeCounter.objects.exists():
            # Create one if it exists
            LifeCounter.objects.create()
            created = True

        life_counter = self.get_queryset().first()
        serializer = self.get_serializer(instance=life_counter)
        status_code = HTTP_201_CREATED if created else HTTP_200_OK
        return Response(data=serializer.data, status=status_code)

    def post(self, request: Request, pk=None):
        pass


## NON REST API
def index(request):
    return render(request, "index.html")
