from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from experchat.permissions import IsUserPermission
from payments.models import Card
from payments.serializers import CardSerializer, NonceSerializer
from payments.utils import ExperchatPayment


class GenerateClientTokenView(APIView):
    """
    API to generate client token for payment method nonce.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'client_token': ExperchatPayment().generate_client_token()})


class CardViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    Viewset to add card, list all cards and delete card.
    """
    queryset = Card.objects.all().order_by('is_default', '-created_timestamp')
    serializer_class = CardSerializer
    permission_classes = (IsUserPermission,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_default', )

    def get_queryset(self):
        queryset = super(CardViewSet, self).get_queryset()
        queryset = queryset.filter(customer__user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card = ExperchatPayment().create_or_update_customer(
            request.user,
            serializer.validated_data['payment_method_nonce']
        )
        serializer = self.serializer_class(card, context=self.get_serializer_context())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ExperchatPayment().delete_card(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'create':
            return NonceSerializer
        return super(CardViewSet, self).get_serializer_class()

    @detail_route(methods=['GET'])
    def make_default(self, request, pk=None, **kwargs):
        card = self.get_object()
        if card.is_default:
            return Response(status=status.HTTP_204_NO_CONTENT)
        ExperchatPayment().make_card_as_default(card)
        return Response(status=status.HTTP_204_NO_CONTENT)
