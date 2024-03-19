from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_205_RESET_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.viewsets import ModelViewSet

from .models import LifeTracker
from .serializers import LifeTrackerSerializer

# Create your views here.


class LifeTrackerViewset(ModelViewSet):
    serializer_class = LifeTrackerSerializer
    queryset = LifeTracker.objects.none()

    def _create_life_tracker(self, data: dict = {}) -> LifeTracker:
        return LifeTracker.objects.create(**data)

    @action(methods=["get", "patch"], detail=False)
    def life_tracker(self, request: Request):
        if request.method == "GET":
            if LifeTracker.objects.exists():
                data = self.get_serializer(instance=LifeTracker.objects.first()).data
                return Response(data=data, status=HTTP_200_OK)

            life_tracker = self._create_life_tracker()

            return Response(
                data=self.get_serializer(instance=life_tracker).data,
                status=HTTP_201_CREATED,
            )
        elif request.method == "PATCH":
            if not LifeTracker.objects.exists():
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        data=serializer.validated_data, status=HTTP_201_CREATED
                    )
                else:
                    return Response(
                        data={"detail": "Bad Request"}, status=HTTP_400_BAD_REQUEST
                    )
            life_tracker = LifeTracker.objects.first()
            serializer = self.get_serializer(instance=life_tracker, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.validated_data, status=HTTP_200_OK)
            else:
                return Response(
                    data={"detail": "Bad Request"}, status=HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data={"detail": "method not allowed"}, status=HTTP_403_FORBIDDEN
            )

    @action(methods=["delete"], detail=False)
    def reset(self, request):
        LifeTracker.objects.all().delete()
        return Response(
            data={
                "detail": "LifeTracker deleted",
            },
            status=HTTP_205_RESET_CONTENT,
        )
