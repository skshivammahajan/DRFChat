from rest_framework import routers

from devices.views import DeviceViewSet

router = routers.SimpleRouter()

router.register(r'devices', DeviceViewSet, base_name='device')

urlpatterns = router.urls
