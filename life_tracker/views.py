from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from .models import LifeTracker
from .serializers import LifeTrackerSerializer


class LifeTrackerViewset(ModelViewSet):
    serializer_class = LifeTrackerSerializer
    queryset = LifeTracker.objects.none()

    @action(methods=["get"], detail=False)
    def life_tracker(self, request):
        if LifeTracker.objects.exists():
            data = self.get_serializer(instance=LifeTracker.objects.first()).data
            return Response(data=data, status=HTTP_200_OK)

        life_tracker = LifeTracker.objects.create()

        return Response(
            data=self.get_serializer(instance=life_tracker).data,
            status=HTTP_201_CREATED,
        )
