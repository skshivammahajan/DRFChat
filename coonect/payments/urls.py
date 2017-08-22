from django.conf.urls import url
from rest_framework import routers

from payments import views

router = routers.SimpleRouter()
router.register(r'cards', views.CardViewSet, base_name='card')
urlpatterns = router.urls


urlpatterns += [
    url(r'^generate-client-token/$', views.GenerateClientTokenView.as_view(), name='get-client-token'),
]
