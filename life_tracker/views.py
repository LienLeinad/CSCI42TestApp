from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from .models import LifeCounter
from .serializers import LifeCounterSerializer

# Create your views here.


class LifeTrackerViewSet(ModelViewSet):
    queryset = LifeCounter.objects.all()  # There really should only be one
    serializer_class = LifeCounterSerializer

    def retrieve(self, request: Request, pk=None):
        life_counter, created = LifeCounter.objects.get_or_create(
            defaults={"p1_life": 40, "p2_life": 40}
        )
        serializer = self.get_serializer(instance=life_counter)
        status_code = HTTP_201_CREATED if created else HTTP_200_OK
        import ipdb

        ipdb.set_trace()
        return Response(data=serializer.data, status=status_code)

    def post(self, request: Request, pk=None):
        pass


def index(request):
    return render(request, "index.html")
