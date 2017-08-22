import random
from unittest import mock

import pytest
from braintree import Transaction as BtTransaction
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from devices.models import Device
from experchat.enumerations import CallStatus
from experchat.models.promocodes import PromoCode
from experchat.models.session_pricing import SessionPricing
from experchat.models.users import User as EcUser
from experchat.models.users import Expert, ExpertProfile
from experchat_sessions import utils
from experchat_sessions.models import Session, SessionTransaction
from experchat_sessions.tasks import calculate_expert_average_rating
from payments.models import Card, Customer, Transaction
from payments.utils import ExperchatPayment
from publisher.utils import ExperchatPublisher
from webrtc.utils import ExperchatWebRTC

User = get_user_model()


@pytest.mark.django_db
class TestUsers(TestCase):
    """
    Unit Test Utility
    """
    # mock publisher class methods
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_user_devices')
    @mock.patch.object(ExperchatPublisher, 'add_push_device')
    @mock.patch.object(ExperchatPublisher, 'remove_push_device')
    def setUp(self, mock_publish_message_on_user_devices,
              mock_add_push_device,
              mock_remove_push_device):
        mock_publish_message_on_user_devices.return_value = True
        mock_add_push_device.return_value = True
        mock_remove_push_device.return_value = True
        self.expert_profile_id = 1
        self.call_delay_time = 10
        self.disconnect_call_initiator = "expert"
        self.tokbox_session_length = 10*60
        self.scheduled_duration = 20
        self.scheduled_duration_price = 30

        SessionPricing.objects.create(session_length=10, price=15)
        SessionPricing.objects.create(session_length=20, price=30)
        SessionPricing.objects.create(session_length=30, price=45)
        SessionPricing.objects.create(session_length=60, price=90)

        # create userbase for user
        self.user = User.objects.create(
            email="testuser@example.com",
            is_email_verified=True
        )
        # create user
        EcUser.objects.create(userbase=self.user)

        # create userbase for expert
        e = User.objects.create(
            email="testexpert@example.com",
            is_email_verified=True
        )

        # create expert
        self.expert = Expert.objects.create(userbase=e)
        self.expert_profile = ExpertProfile.objects.create(expert=self.expert)

        # create expert and user devices
        self.user_device = Device.objects.create(user=User.objects.get(email='testuser@example.com'),
                                                 device_id='user_device_id',
                                                 device_token='user_device_token')
        self.expert_device = Device.objects.create(user=User.objects.get(email='testexpert@example.com'),
                                                   device_id='expert_device_id',
                                                   device_token='expert_device_token'
                                                   )
        self.scheduled_datetime = timezone.now() + timezone.timedelta(seconds=30)

        # create new session
        self.session_obj = Session.objects.create(
            expert_profile=self.expert_profile,
            expert=self.expert,
            user=self.user,
            user_device=self.user_device,
            scheduled_duration=self.scheduled_duration,
            estimated_revenue=30,
            scheduled_datetime=self.scheduled_datetime,
        )

    def test_initiate_call(self):
        assert self.session_obj.call_status == CallStatus.INITIATED.value

    # mock webrtc and publisher methods
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session')
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session_token')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    def test_accept_call(self, mock_publish_message_on_device,
                         mock_get_webrtc_session,
                         mock_get_webrtc_session_token):
        mock_publish_message_on_device.return_value = True
        mock_get_webrtc_session_token.return_value = "webrtc_token"
        mock_get_webrtc_session.return_value = "webrtc_session"

        # Verify accept call status
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.call_status == CallStatus.ACCEPTED.value

        # Verify after accept call no delay or decline can be performed
        self.session_obj.delay_call(self.call_delay_time)
        assert self.session_obj.call_status == CallStatus.ACCEPTED.value

        self.session_obj.decline_call()
        assert self.session_obj.call_status == CallStatus.ACCEPTED.value

        # Verify disconnect after accept call
        self.session_obj.disconnect_call(self.disconnect_call_initiator,
                                         self.tokbox_session_length)
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

    # mock publisher method
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    def test_declined_call(self, mock_publish_message_on_device):
        mock_publish_message_on_device.return_value = True

        # Verify decline call status
        self.session_obj.decline_call()
        assert self.session_obj.call_status == CallStatus.DECLINED.value

        # Verify that no accept/delay/disconnect can be performed after decline
        # status
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.call_status == CallStatus.DECLINED.value

        self.session_obj.delay_call(self.call_delay_time)
        assert self.session_obj.call_status == CallStatus.DECLINED.value

        self.session_obj.disconnect_call(self.disconnect_call_initiator,
                                         self.tokbox_session_length)
        assert self.session_obj.call_status == CallStatus.DECLINED.value

    # mock publisher method
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    def test_delay_call(self, mock_publish_message_on_device):
        mock_publish_message_on_device.return_value = True

        # Verify delay call status
        self.session_obj.delay_call(self.call_delay_time)
        assert self.session_obj.call_status == CallStatus.DELAYED.value

        # Verify that no accept/decline/disconnect can be performed after delay
        # status
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.call_status == CallStatus.DELAYED.value

        self.session_obj.decline_call()
        assert self.session_obj.call_status == CallStatus.DELAYED.value

        self.session_obj.disconnect_call(self.disconnect_call_initiator,
                                         self.tokbox_session_length)
        assert self.session_obj.call_status == CallStatus.DELAYED.value

    # mock webrtc and publisher methods
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session')
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session_token')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_user_devices')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    def test_disconnect_call_from_accept(
            self, mock_publish_message_on_user_devices,
            mock_publish_message_on_device,
            mock_get_webrtc_session,
            mock_get_webrtc_session_token
    ):
        mock_publish_message_on_user_devices.return_value = True
        mock_publish_message_on_device.return_value = True
        mock_get_webrtc_session_token.return_value = "webrtc_token"
        mock_get_webrtc_session.return_value = "webrtc_session"

        # Accept call to disconnect
        self.session_obj.accept_call(expert_device=self.expert_device)
        self.session_obj.disconnect_call(self.disconnect_call_initiator,
                                         self.tokbox_session_length)
        # Verify disconnection status
        assert self.session_obj.call_status == CallStatus.COMPLETED.value
        assert self.session_obj.tokbox_session_length == self.tokbox_session_length

        # Verify after disconnection, no other action can be performed.
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

        self.session_obj.decline_call()
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

        self.session_obj.delay_call(self.call_delay_time)
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

    # mock publisher method
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_user_devices')
    def test_disconnect_call(self, mock_publish_message_on_user_devices, mock_publish_message_on_device):
        mock_publish_message_on_user_devices.return_value = True
        mock_publish_message_on_device.return_value = True

        # Verify disconnect status and tokbox_session_length
        self.session_obj.disconnect_call(self.disconnect_call_initiator,
                                         self.tokbox_session_length)
        assert self.session_obj.call_status == CallStatus.COMPLETED.value
        assert self.session_obj.tokbox_session_length == self.tokbox_session_length

        # Verify after disconnection, no other action can be performed.
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

        self.session_obj.decline_call()
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

        self.session_obj.delay_call(self.call_delay_time)
        assert self.session_obj.call_status == CallStatus.COMPLETED.value

    def test_delete_scheduled_call(self):
        self.session_obj.delete()
        assert self.session_obj.is_deleted and self.session_obj.id is not None

    # mock webrtc and publisher methods
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session')
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session_token')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_user_devices')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    def test_revenue_call(
            self, mock_publish_message_on_user_devices,
            mock_publish_message_on_device,
            mock_get_webrtc_session,
            mock_get_webrtc_session_token
    ):
        mock_publish_message_on_user_devices.return_value = True
        mock_publish_message_on_device.return_value = True
        mock_get_webrtc_session_token.return_value = "webrtc_token"
        mock_get_webrtc_session.return_value = "webrtc_session"

        # Accept call
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.revenue == 0

        self.session_obj.disconnect_call(self.disconnect_call_initiator, 4*60)
        assert self.session_obj.revenue == 0

    # mock webrtc and publisher methods
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session')
    @mock.patch.object(ExperchatWebRTC, 'get_webrtc_session_token')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_user_devices')
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_device')
    def test_revenue_after_extend_call(
            self, mock_publish_message_on_user_devices,
            mock_publish_message_on_device,
            mock_get_webrtc_session,
            mock_get_webrtc_session_token
    ):
        mock_publish_message_on_user_devices.return_value = True
        mock_publish_message_on_device.return_value = True
        mock_get_webrtc_session_token.return_value = "webrtc_token"
        mock_get_webrtc_session.return_value = "webrtc_session"

        # Accept call
        self.session_obj.accept_call(expert_device=self.expert_device)
        assert self.session_obj.revenue == 0

        self.session_obj.extend_session()

        self.session_obj.disconnect_call(self.disconnect_call_initiator, 22*60)
        assert self.session_obj.revenue == self.scheduled_duration_price + settings.SESSION_EXTENSION_PRICE


@pytest.mark.django_db
class TestPayment(TestCase):
    """
    Unit Test Utility for payment.
    """

    # mock publisher class methods
    @mock.patch.object(ExperchatPublisher, 'publish_message_on_user_devices')
    @mock.patch.object(ExperchatPublisher, 'add_push_device')
    @mock.patch.object(ExperchatPublisher, 'remove_push_device')
    def setUp(self, mock_publish_message_on_user_devices,
              mock_add_push_device,
              mock_remove_push_device):
        mock_publish_message_on_user_devices.return_value = True
        mock_add_push_device.return_value = True
        mock_remove_push_device.return_value = True

        # create userbase for user
        self.user = User.objects.create(
            email="testuser@example.com",
            is_email_verified=True
        )
        # create user
        EcUser.objects.create(userbase=self.user)

        # create userbase for expert
        e = User.objects.create(
            email="testexpert@example.com",
            is_email_verified=True
        )

        # create expert
        self.expert = Expert.objects.create(userbase=e)
        self.expert_profile = ExpertProfile.objects.create(expert=self.expert)

        # create expert and user devices
        self.user_device = Device.objects.create(user=User.objects.get(email='testuser@example.com'),
                                                 device_id='user_device_id',
                                                 device_token='user_device_token')

        self.scheduled_datetime = timezone.now() + timezone.timedelta(seconds=30)
        self.card = None

        # create new session
        self.session_obj = Session.objects.create(
            expert_profile=self.expert_profile,
            expert=self.expert,
            user=self.user,
            user_device=self.user_device,
        )

        # create new customer
        self.customer = Customer.objects.create(
            user=self.session_obj.user,
            customer_uid='fghdjh',
        )

        # create new card
        self.card = Card.objects.create(
            customer=self.customer,
            last_4='1111',
            payment_method_token='payment_method_token',
            card_type='card_type',
            expiration_date='11/2020',
            is_default=True,
        )

    # mock braintree methods
    @mock.patch.object(ExperchatPayment, 'create_pre_auth_transaction')
    @mock.patch.object(BtTransaction, 'void')
    def test_payment_status_after_scheduling_the_call(self, mock_void, mock_create_pre_auth_transaction):
        mock_create_pre_auth_transaction.return_value = "123"
        mock_void.return_value = mock.MagicMock(is_success=True)

        # Do pre authorization for payment of session
        transaction = ExperchatPayment().create_pre_auth_transaction_from_card(
            self.session_obj.user,
            self.session_obj.estimated_revenue,
            self.card,
        )

        SessionTransaction.objects.create(session=self.session_obj, session_event_type='scheduled',
                                          transaction=transaction)

        assert transaction.status == Transaction.UNSETTLED

        # cancel the user transaction
        ExperchatPayment().cancel_user_transactions(self.session_obj.user)
        updated_transaction = Transaction.objects.get(id=transaction.id)

        assert updated_transaction.status == Transaction.CANCELLED

    # mock braintree methods
    @mock.patch.object(ExperchatPayment, 'create_pre_auth_transaction')
    @mock.patch.object(BtTransaction, 'submit_for_settlement')
    def test_payment_status_of_the_settled_call(self, mock_submit_for_settlement, mock_create_pre_auth_transaction):
        mock_create_pre_auth_transaction.return_value = "123"
        mock_submit_for_settlement.return_value = mock.MagicMock(is_success=True)

        transaction = ExperchatPayment().create_pre_auth_transaction_from_card(
            self.session_obj.user,
            self.session_obj.estimated_revenue,
            self.card,
        )

        SessionTransaction.objects.create(session=self.session_obj, session_event_type='scheduled',
                                          transaction=transaction)

        assert transaction.status == Transaction.UNSETTLED

        # settle the user payment
        ExperchatPayment().settle_user_transactions(self.session_obj.user)
        updated_transaction = Transaction.objects.get(id=transaction.id)

        assert updated_transaction.status == Transaction.SETTLED


@pytest.mark.django_db
class TestExpertAvgRatingUtil(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com')
        self.expert = Expert.objects.create(userbase=self.user)
        number_of_ratings = random.randint(10, 20)
        self.ratings = [random.randint(1, 5) for i in range(number_of_ratings)]

    def test_avg_rating_util(self):
        for rating in self.ratings:
            calculate_expert_average_rating(self.expert.id, rating)
        expert = Expert.objects.get(userbase=self.expert.id)

        assert round(sum(self.ratings) / len(self.ratings)) == round(expert.avg_rating)\
            and expert.num_rating == len(self.ratings)


@pytest.mark.django_db
class TestCoupanCodeUtils(TestCase):
    """
    Test case for testing the Promo code related utils
    """
    def setUp(self):
        self.session_price = 100
        self.user1 = User.objects.create(email='testuser@example.com')
        self.user2 = User.objects.create(email='testuser2@example.com')
        self.user3 = User.objects.create(email='testuser3@example.com')
        self.EcUser1 = EcUser.objects.create(userbase=self.user1)
        self.EcUser2 = EcUser.objects.create(userbase=self.user2)
        self.EcUser3 = EcUser.objects.create(userbase=self.user3)
        self.expert1 = Expert.objects.create(userbase=self.user1)
        self.expert2 = Expert.objects.create(userbase=self.user2)
        self.expert3 = Expert.objects.create(userbase=self.user3)
        start_date_time = timezone.datetime.strptime('2017-05-15 5:30', "%Y-%m-%d %H:%M")
        expiry_datetime = timezone.datetime.strptime('2017-05-25 12:30', "%Y-%m-%d %H:%M")
        self.valid_schedule_datetime = timezone.datetime.strptime('2017-05-20 6:30', "%Y-%m-%d %H:%M")
        self.invalid_schedule_datetime = timezone.datetime.strptime('2017-05-14 4:30', "%Y-%m-%d %H:%M")
        self.descriptions = ["Promo Code, Offer", "Credit type"]
        self.value_type = [PromoCode.PERCENT_OFFER, PromoCode.FIXED_PRICE_OFFER]
        self.promo_code_type = [PromoCode.PROMO, PromoCode.CREDIT]
        self.promo_code_status = [PromoCode.ACTIVE, PromoCode.INACTIVE]
        self.valid_coupon_codes = ['AHFHFH50', 'OFFER30']
        self.invalid_coupon_code = 'HDDOFFER30'
        self.allowed_experts = [self.expert1, self.expert2]
        self.allowed_users = [self.EcUser1, self.EcUser2]
        self.user_uses_limits = [2, 2]
        # create promo codes
        for i in range(2):
            promo_code = PromoCode.objects.create(
                promo_code_type=self.promo_code_type[i],
                value_type=self.value_type[i],
                value=100,
                start_datetime=start_date_time,
                expiry_datetime=expiry_datetime,
                usage_limit=3,
                description=self.descriptions[i],
                coupon_code=self.valid_coupon_codes[i],
                status=self.promo_code_status[i],
                is_deleted=False,
                user_usage_limit=self.user_uses_limits[i]
            )
            promo_code.allowed_experts.add(*self.allowed_experts)
            promo_code.allowed_users.add(*self.allowed_users)
            promo_code.save()

        # create the Customer
        self.customer = Customer.objects.create(
            user=self.user1,
            customer_uid='JDJKDKJDJK787878',
        )
        # Craete the card
        self.card = Card.objects.create(
            customer=self.customer,
            last_4='1111',
            payment_method_token='payment_method_token',
            card_type='card_type',
            expiration_date='11/2020',
            is_default=True,
        )
        # Create the Transactions for first promo code
        self.transactions = Transaction.objects.create(
            user=self.user1,
            card=self.card,
            transaction_uid='',
            status=Transaction.UNSETTLED,
            amount=23,
            promo_code=PromoCode.objects.get(coupon_code=self.valid_coupon_codes[0])
        )

    def test_is_valid_promocode_with_invalid_promo_code(self):
        """
        Test case for validating a promo code with invalid data
        """
        is_valid = utils.is_valid_promocode(
            self.EcUser1, self.invalid_coupon_code, self.expert1.id,
            timezone.make_aware(self.valid_schedule_datetime, timezone=timezone.pytz.UTC)
        )
        assert not is_valid

    def test_is_valid_promocode_when_promocode_is_inactive(self):
        """
        Test case for validating a promo code when used promo code is inactive
        """
        is_valid = utils.is_valid_promocode(
            self.EcUser1, self.valid_coupon_codes[1], self.expert1.id,
            timezone.make_aware(self.valid_schedule_datetime, timezone=timezone.pytz.UTC)
        )
        assert not is_valid

    def test_is_valid_promocode_with_invalid_schedule_datetime(self):
        """
        Test case for validating a promo code with invalid schedule_datetime
        """
        is_valid = utils.is_valid_promocode(
            self.EcUser1, self.valid_coupon_codes[0], self.expert1.id,
            timezone.make_aware(self.invalid_schedule_datetime, timezone=timezone.pytz.UTC)
        )
        assert not is_valid

    def test_is_valid_promocode_with_invalid_expert(self):
        """
        Test case for validating a promo code with invalid expert
        """
        is_valid = utils.is_valid_promocode(
            self.EcUser1, self.valid_coupon_codes[0], self.expert3.id,
            timezone.make_aware(self.valid_schedule_datetime, timezone=timezone.pytz.UTC)
        )
        assert not is_valid

    def test_is_valid_promocode_with_invalid_user(self):
        """
        Test case for validating a promo code with invalid user
        """
        is_valid = utils.is_valid_promocode(
            self.EcUser3, self.valid_coupon_codes[0], self.expert1.id,
            timezone.make_aware(self.valid_schedule_datetime, timezone=timezone.pytz.UTC)
        )
        assert not is_valid

    def test_is_valid_promocode(self):
        """
        Test case for validating a promo code with success
        """
        is_valid = utils.is_valid_promocode(
            self.EcUser1, self.valid_coupon_codes[0], self.expert1.id,
            timezone.make_aware(self.valid_schedule_datetime, timezone=timezone.pytz.UTC)
        )
        assert is_valid is True

    def test_validate_coupon_code_amount_used_without_transactions(self):
        """
        Test validate_coupon_code_amount withput transactions
        """
        promo_code_obj = PromoCode.objects.get(coupon_code=self.valid_coupon_codes[1])
        result = utils.validate_coupon_code_amount_used(promo_code_obj)
        assert result is True

    def test_validate_coupon_code_amount_used_with_transactions(self):
        """
        Test validate_coupon_code_amount with transactions
        """
        promo_code_obj = PromoCode.objects.get(coupon_code=self.valid_coupon_codes[0])
        result = utils.validate_coupon_code_amount_used(promo_code_obj)
        assert result is True

    def test_validate_coupon_code_amount_used_with_transactions_type_credit(self):
        """
        Test validate_coupon_code_amount with transactions and type is credit
        """
        # Create the Transactions for first promo code
        Transaction.objects.create(
            user=self.user2,
            card=self.card,
            transaction_uid='',
            status=Transaction.UNSETTLED,
            amount=40,
            promo_code=PromoCode.objects.get(coupon_code=self.valid_coupon_codes[1])
        )
        promo_code_obj = PromoCode.objects.get(coupon_code=self.valid_coupon_codes[1])
        result = utils.validate_coupon_code_amount_used(promo_code_obj)
        assert result

    def test_calculate_used_promo_code_amount(self):
        """
        Test for calculate_used_promo_code_amount
        """
        promo_code_obj = PromoCode.objects.get(coupon_code=self.valid_coupon_codes[0])
        promo_code_transactions = promo_code_obj.transactions.all().filter(
            status__in=[Transaction.UNSETTLED, Transaction.SETTLED]
        )
        result = utils.calculate_used_promo_code_amount(promo_code_transactions)
        assert result == 23

    def test_calculate_discount_price_when_type_is_credit(self):
        """
        Test case for calculating the discount price when promo code type is credit
        """
        Transaction.objects.create(
            user=self.user2,
            card=self.card,
            transaction_uid='',
            status=Transaction.UNSETTLED,
            amount=40,
            promo_code=PromoCode.objects.get(coupon_code=self.valid_coupon_codes[1])
        )

        result = utils.calculate_discount_price(self.valid_coupon_codes[1], self.session_price)
        assert result == 60

    def test_calculate_discount_price_when_type_is_credit_with_all_consumed(self):
        """
        Test case for calculating the discount price when promo code type is credit when all amount is
        used by promo code
        """
        Transaction.objects.create(
            user=self.user2,
            card=self.card,
            transaction_uid='',
            status=Transaction.UNSETTLED,
            amount=20,
            promo_code=PromoCode.objects.get(coupon_code=self.valid_coupon_codes[1])
        )
        result = utils.calculate_discount_price(self.valid_coupon_codes[1], self.session_price)
        assert result == 80

    def test_calculate_discount_price_when_type_is_promocode(self):
        """
        Test case for calculating the discount price when promo code type is promo
        """
        result = utils.calculate_discount_price(self.valid_coupon_codes[0], self.session_price)
        assert result == 100
