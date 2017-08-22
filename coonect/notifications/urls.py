from rest_framework import routers

from notifications.views import NotificationViewSet

router = routers.SimpleRouter()

router.register(r'notifications', NotificationViewSet, base_name='notification')

urlpatterns = router.urls
