from rest_framework import mixins, permissions, viewsets

from devices.enumerations import DeviceStatus
from devices.models import Device
from devices.serializers import DeviceSerializer


class DeviceViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Allow user to manage self owned devices.
    """
    serializer_class = DeviceSerializer
    queryset = Device.objects.filter(status=DeviceStatus.ACTIVE.value)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(DeviceViewSet, self).get_queryset()

        queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
