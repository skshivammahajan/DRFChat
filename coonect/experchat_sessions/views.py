from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError
from django.db.models import Case, CharField, Value, When
from django.http import Http404
from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, detail_route, list_route, renderer_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from experchat.enumerations import CallStatus
from experchat.messages import get_message
from experchat.models.promocodes import PromoCode
from experchat.models.session_pricing import SessionPricing
from experchat.permissions import IsExpertPermission, IsUserPermission
from experchat.serializers import EmptySerializer, SessionRatingSerializer
from experchat.views import ExperChatAPIView
from experchat_sessions import tasks
from experchat_sessions.enumerations import SessionListStatus
from experchat_sessions.exceptions import InvalidPreAuthException
from experchat_sessions.models import Session, SessionTransaction
from experchat_sessions.serializers import (
    AcceptSerializer, ApplyPromoCodeSerializer, DelaySerializer, DisconnectSerializer, ScheduleSessionSerializer,
    SessionListSerializer, SessionSerializer, SwitchDeviceSerializer, ValidatePromoCodeSerializer
)
from experchat_sessions.tasks import calculate_expert_average_rating
from experchat_sessions.utils import SessionEventsProcess, calculate_discount_price
from notifications.models import Activity
from payments.models import Card, Transaction
from payments.utils import ExperchatPayment


class SessionViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    permission_classes = (IsUserPermission,)

    def get_queryset(self):
        queryset = super(SessionViewSet, self).get_queryset()

        if hasattr(self.request.user, 'expert'):
            queryset = queryset.filter(expert=self.request.user.expert)
        elif hasattr(self.request.user, 'user'):
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_initiator(self):
        user_type = 'expert' if hasattr(self.request.user, 'expert') else 'user'
        return user_type

    @detail_route(methods=['put'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def initialize(self, request, pk=None):
        obj = self.get_object()
        obj.initialize()
        return Response({"status": obj.call_status})

    @detail_route(methods=['put'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def reconnect(self, request, pk=None):
        obj = self.get_object()
        obj.reconnect()
        return Response({"status": obj.call_status})

    @detail_route(methods=['delete'], permission_classes=(IsExpertPermission,))
    def decline(self, request, pk=None):
        session_obj = self.get_object()
        session_obj.decline_call()
        decline_response = {"status": session_obj.call_status}
        return Response(decline_response)

    @detail_route(methods=['put'], permission_classes=(IsExpertPermission,), serializer_class=DelaySerializer)
    def delay(self, request, pk=None):
        session_obj = self.get_object()
        serializer = DelaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_obj.delay_call(serializer.validated_data['delay_time'])
        delay_response = {"status": session_obj.call_status}
        return Response(delay_response)

    @detail_route(methods=['post'], permission_classes=(IsExpertPermission,), serializer_class=AcceptSerializer)
    def accept(self, request, pk=None):
        session_obj = self.get_object()

        serializer = AcceptSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        session_info = session_obj.accept_call(serializer.validated_data['expert_device'])
        accept_response = {
            'status': session_obj.call_status,
            'data': session_info
        }
        return Response(accept_response)

    @detail_route(methods=['delete'], permission_classes=(permissions.IsAuthenticated,),
                  serializer_class=DisconnectSerializer)
    def disconnect(self, request, pk=None):
        session_obj = self.get_object()
        serializer = DisconnectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_obj.disconnect_call(
            'expert' if hasattr(request.user, 'expert') else 'user',
            serializer.validated_data['tokbox_session_length']
        )
        disconnect_response = {"status": session_obj.call_status}
        return Response(disconnect_response)

    @detail_route(methods=['put'], permission_classes=(IsUserPermission,), serializer_class=EmptySerializer)
    def extend_session(self, request, pk=None):
        session_obj = self.get_object()
        if session_obj.call_status == CallStatus.ACCEPTED:

            # pre-authorization of payment
            card = Card.objects.filter(id=session_obj.card).first()
            transaction = ExperchatPayment().create_pre_auth_transaction_from_card(request.user,
                                                                                   settings.SESSION_EXTENSION_PRICE,
                                                                                   card)
            if not transaction:
                raise InvalidPreAuthException
            session_obj.extend_session()
            SessionTransaction.objects.create(session=session_obj,
                                              session_event_type='extend session',
                                              transaction=transaction)

        update_response = {
            "extended_duration": session_obj.extended_duration
            }
        return Response(update_response)

    @detail_route(methods=['post'], permission_classes=(IsExpertPermission,), serializer_class=SwitchDeviceSerializer)
    def switch_device(self, request, pk=None):
        session_obj = self.get_object()
        if session_obj.call_status == CallStatus.ACCEPTED:
            serializer = SwitchDeviceSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            session_obj.switch_device(serializer.validated_data['device_id'])
        switch_response = {"status": session_obj.call_status}
        return Response(switch_response)

    @detail_route(methods=['post'], permission_classes=(IsUserPermission,),
                  serializer_class=SessionRatingSerializer)
    def review(self, request, pk=None):
        session_obj = self.get_object()
        if session_obj.call_status != CallStatus.COMPLETED:
            raise Http404

        serializer = SessionRatingSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            review = serializer.save(session=session_obj)
            calculate_expert_average_rating.delay(session_obj.expert_id, serializer.validated_data['overall_rating'])
        except IntegrityError:
            return Response({
                "errors": {
                    api_settings.NON_FIELD_ERRORS_KEY: [get_message('ERROR_REVIEW_ALREADY_SUBMITTED')]
                }
            })

        Activity.objects.create(
            actor=request.user,
            notify_to=session_obj.expert.userbase,
            code='review-session',
            data={
                "expert": {
                    "name": session_obj.expert.userbase.name,
                    "display_name": session_obj.expert.display_name,
                    "profile_photo": session_obj.expert.userbase.profile_photo,
                },
                "user": {
                    "name": session_obj.user.name,
                    "display_name": session_obj.user.user.display_name,
                    "profile_photo": session_obj.user.profile_photo,
                },
                "scheduled_datetime": DateTimeField().to_representation(session_obj.scheduled_datetime),
                "title": session_obj.title,
                "scheduled_duration": session_obj.scheduled_duration,
                "estimated_revenue": str(session_obj.estimated_revenue),
                "session_review_overall_rating": review.overall_rating,
                "session_review_comment": review.text_review,
                "session_id": session_obj.id
            }
        )

        return Response(serializer.data)

    @list_route(methods=['post'], permission_classes=(IsUserPermission,), serializer_class=ScheduleSessionSerializer)
    def schedule(self, request):
        serializer = ScheduleSessionSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        # pre-authorization of payment
        # add the promocode in the transaction

        pre_auth_amount = 0
        discount_price = 0
        promo_code_obj = None
        if request.data.get('promo_code'):
            # at this point we are sure that used coupon code is a valid coupon code, that's why getting directly w
            # without exception handling
            promo_code_obj = \
                PromoCode.objects.filter(coupon_code=serializer.validated_data['promo_code']).first()

            discount_price = calculate_discount_price(
                promo_code_obj.coupon_code, serializer.validated_data['estimated_revenue']
            )
            revenue_after_discount = serializer.validated_data['estimated_revenue'] - discount_price
            if revenue_after_discount <= 0:
                pre_auth_amount = (
                    float(serializer.validated_data['estimated_revenue']) *
                    settings.SESSION_CANCELLATION_PERCENTAGE_AMOUNT / 100
                )
            else:
                pre_auth_amount = revenue_after_discount

        else:
            pre_auth_amount = serializer.validated_data['estimated_revenue']

        card = Card.objects.filter(id=serializer.validated_data.get('card')).first()
        transaction = ExperchatPayment().create_pre_auth_transaction_from_card(
            request.user,
            pre_auth_amount,
            card
        )
        if not transaction:
            raise InvalidPreAuthException

        session = serializer.save(user=request.user, call_status=CallStatus.SCHEDULED.value)
        # create the entry in Transaction table for Promocode once call is scheduled
        if request.data.get('promo_code'):
            tns = Transaction.objects.create(
                user=request.user,
                transaction_uid='',
                amount=discount_price,
                promo_code=promo_code_obj
            )
            SessionTransaction.objects.create(session=session, session_event_type='scheduled', transaction=tns)

        # Call celery task to adjust payment in case of missed call
        call_missed_time = serializer.validated_data.get('scheduled_datetime') + \
            timezone.timedelta(seconds=settings.SESSION_GRACE_DURATION)
        tasks.cancel_payment_on_user_missed.apply_async((session.id,), eta=call_missed_time)
        SessionTransaction.objects.create(session=session, session_event_type='scheduled', transaction=transaction)

        data = {
            "expert": {
                "name": session.expert.userbase.name,
                "display_name": session.expert.display_name,
                "profile_photo": session.expert.userbase.profile_photo,
            },
            "user": {
                "name": request.user.name,
                "display_name": request.user.user.display_name,
                "profile_photo": request.user.profile_photo,
            },
            "scheduled_datetime": DateTimeField().to_representation(session.scheduled_datetime),
            "title": session.title,
            "scheduled_duration": session.scheduled_duration,
            "estimated_revenue": str(session.estimated_revenue),
            "session_id": session.id
        }

        # Notification to Expert
        Activity.objects.create(
            actor=request.user,
            notify_to=session.expert.userbase,
            code='schedule-session-expert',
            data=data
        )

        data.update(
            attachments=[
                "experchat_sessions/templates/notifications/email/attachments/Session Prep Doc.pdf"
            ]
        )
        # Notification to User
        Activity.objects.create(
            actor=request.user,
            notify_to=session.user,
            code='schedule-session-user',
            data=data
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @detail_route(methods=['delete'], permission_classes=(permissions.IsAuthenticated,))
    def cancel(self, request, pk=None):
        session_obj = self.get_object()
        if session_obj.call_status == CallStatus.SCHEDULED and session_obj.scheduled_datetime > timezone.now():
            session_obj.cancel_session()
            if hasattr(self.request.user, 'user'):
                notify_to = session_obj.expert.userbase
                code = 'cancel-session-expert'
            else:
                notify_to = session_obj.user
                code = 'cancel-session-user'
            Activity.objects.create(
                actor=request.user,
                notify_to=notify_to,
                code=code,
                data={
                    "expert": {
                        "name": session_obj.expert.userbase.name,
                        "display_name": session_obj.expert.display_name,
                        "profile_photo": session_obj.expert.userbase.profile_photo,
                    },
                    "user": {
                        "name": session_obj.user.name,
                        "display_name": session_obj.user.user.display_name,
                        "profile_photo": session_obj.user.profile_photo,
                    },
                    "scheduled_datetime": DateTimeField().to_representation(session_obj.scheduled_datetime),
                    "title": session_obj.title,
                    "scheduled_duration": session_obj.scheduled_duration,
                    "estimated_revenue": str(session_obj.estimated_revenue),
                    "session_id": session_obj.id
                }
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    @detail_route(methods=['put'], permission_classes=(IsUserPermission,), serializer_class=ApplyPromoCodeSerializer)
    def apply_promo_code(self, request, pk=None):
        session = self.get_object()
        serializer = self.serializer_class(data=request.data, context={"request": request, "pk": pk})
        serializer.is_valid(raise_exception=True)
        pre_auth_amount = 0
        promo_code_obj = PromoCode.objects.filter(coupon_code=serializer.validated_data['promo_code']).first()
        discount_price = calculate_discount_price(
            promo_code_obj.coupon_code, session.estimated_revenue
        )
        revenue_after_discount = session.estimated_revenue - discount_price
        if revenue_after_discount <= 0:
            pre_auth_amount = (
                float(session.estimated_revenue) *
                settings.SESSION_CANCELLATION_PERCENTAGE_AMOUNT / 100
            )
        else:
            pre_auth_amount = revenue_after_discount

        card = Card.objects.filter(id=session.card).first()
        session_transaction = SessionTransaction.objects.filter(
            session_id=session.id, transaction__status=Transaction.UNSETTLED
        )
        for transaction in session_transaction:
            ExperchatPayment().cancel_transaction(transaction=transaction.transaction)

        transaction = ExperchatPayment().create_pre_auth_transaction_from_card(
            request.user,
            pre_auth_amount,
            card
        )
        if not transaction:
            raise InvalidPreAuthException

        SessionTransaction.objects.create(session=session, session_event_type='scheduled', transaction=transaction)
        # create the transaction for promocode
        tns = Transaction.objects.create(
            user=request.user,
            transaction_uid='',
            amount=discount_price,
            promo_code=promo_code_obj
        )
        SessionTransaction.objects.create(session=session, session_event_type='scheduled', transaction=tns)
        # update the session data with promocode
        session.promo_code = serializer.validated_data['promo_code']
        session.save()

        return Response(status=status.HTTP_200_OK, data=ScheduleSessionSerializer(session).data)

    @detail_route(methods=['delete'], permission_classes=(IsUserPermission,),)
    def remove_promo_code(self, request, pk=None):
        session = self.get_object()
        if not session.promo_code:
            return Response(status=status.HTTP_204_NO_CONTENT)

        discount_price = calculate_discount_price(
            session.promo_code, session.estimated_revenue
        )
        pre_auth_amount = session.estimated_revenue + discount_price
        card = Card.objects.filter(id=session.card).first()
        session_transaction = SessionTransaction.objects.filter(
            session_id=session.id,
            transaction__status=Transaction.UNSETTLED
        )
        for transaction in session_transaction:
            if transaction.transaction.promo_code:
                transaction.transaction.status = Transaction.CANCELLED
                transaction.transaction.save()
            else:
                ExperchatPayment().cancel_transaction(transaction=transaction.transaction)

        # create a new transaction with updated preauth amount
        transaction = ExperchatPayment().create_pre_auth_transaction_from_card(
            request.user,
            pre_auth_amount,
            card
        )
        if not transaction:
            raise InvalidPreAuthException

        # Create the SessionTransaction for new transaction
        SessionTransaction.objects.create(session=session, session_event_type='scheduled', transaction=transaction)
        # remove the promo_code from session
        session.promo_code = None
        session.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@renderer_classes((JSONRenderer,))
def callback(request):
    """
    This function is to serv webhook hits.
    :param request:
    Params are according to the event happening on webrtc server.
    :return:
    json response. {"status": "Webhook received."}
    """
    if request.data:
        SessionEventsProcess(request.data).process_events()

    return Response({"status": "Webhook received."})


class SessionPriceView(APIView):
    """
    View to list all session prices.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        queryset = SessionPricing.objects.values('session_length', 'price')
        price_list = list(queryset)
        session_extend_matrix = {"session_extension_time": settings.SESSION_EXTENSION_TIME,
                                 "session_extension_price": settings.SESSION_EXTENSION_PRICE}

        return Response({
            "sessions": price_list,
            "session_extension": session_extend_matrix
        })


class SessionListView(viewsets.ReadOnlyModelViewSet):
    """
    View for Listing all the Sessions on the basis of filters.

    **Query Parameters**

       -  `status` -- _session status_, (ex: 'in-progress', 'completed', 'scheduled', 'user-missed', 'expert-missed',
       'cancelled')

    """
    queryset = Session.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SessionListSerializer

    def get_queryset(self):
        queryset = super(SessionListView, self).get_queryset()
        if hasattr(self.request.user, 'expert'):
            queryset = queryset.filter(expert=self.request.user.expert)
        else:
            queryset = queryset.filter(user=self.request.user)

        if self.kwargs.get('session_type', '') == 'past':
            queryset = queryset.filter(
                scheduled_datetime__lt=timezone.now() - timedelta(seconds=settings.SESSION_GRACE_DURATION)
            ).order_by('-scheduled_datetime')
        elif self.kwargs.get('session_type', '') == 'future':
            queryset = queryset.filter(
                scheduled_datetime__gte=timezone.now() - timedelta(seconds=settings.SESSION_GRACE_DURATION)
            ).order_by('scheduled_datetime')

        queryset = queryset.annotate(
            status=Case(
                When(call_status=CallStatus.SCHEDULED, is_deleted=True, then=Value(SessionListStatus.CANCELLED.value)),
                When(scheduled_datetime__lt=timezone.now() - timedelta(seconds=settings.SESSION_GRACE_DURATION),
                     call_status=CallStatus.INITIATED.value, then=Value(SessionListStatus.EXPERT_MISSED.value)),
                When(call_status__in=[CallStatus.ACCEPTED, CallStatus.INITIATED],
                     then=Value(SessionListStatus.INPROGRESS.value)),
                When(scheduled_datetime__lt=timezone.now() - timedelta(seconds=settings.SESSION_GRACE_DURATION),
                     call_status=CallStatus.SCHEDULED.value, then=Value(SessionListStatus.USER_MISSED.value)),
                When(call_status=CallStatus.SCHEDULED, is_deleted=False, then=Value(SessionListStatus.SCHEDULED.value)),
                default=Value(SessionListStatus.COMPLETED.value),
                output_field=CharField(),
            ),
        )

        session_status = [i.value for i in SessionListStatus.__members__.values()]

        status = self.request.query_params.get('status', '')
        if status in session_status:
            # Filter on the basis of Session Status
            queryset = queryset.filter(status=status)

        return queryset


class ValidatePromoCodeView(ExperChatAPIView):
    """
    View for Validating the promo_code entered by User
    """
    permission_classes = (IsUserPermission,)
    serializer_class = ValidatePromoCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
