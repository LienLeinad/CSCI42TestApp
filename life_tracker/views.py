from django.shortcuts import render
from rest_framework.decorators import action
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

        life_counter = (
            LifeCounter.objects.first()
        )  # There should, in any case, only be one
        serializer = self.get_serializer(instance=life_counter)
        status_code = HTTP_201_CREATED if created else HTTP_200_OK
        return Response(data=serializer.data, status=status_code)

    @action(methods=["post"], detail=False, url_name="reset")
    def reset(self, request: Request):
        LifeCounter.objects.all().delete()  # Deletes all LifeCounter objects
        life_counter = LifeCounter.objects.create()  # Creates a new life counter object

        serializer = self.get_serializer(instance=life_counter)

        return Response(data=serializer.data)


## NON REST API
def index(request):
    return render(request, "index.html")
