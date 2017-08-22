from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.utils import timezone

from experchat.enumerations import CallStatus
from experchat.models.stats import DailyExpertStats
from experchat.models.users import Expert
from payments.models import Transaction
from payments.utils import ExperchatPayment


@shared_task
def calculate_daily_expert_session_stats(expert_id, revenue):
    """
    Task to Calculate daily Stats for completed sessions of experts.
    """
    expert = Expert.objects.get(userbase=expert_id)
    expert_stats_obj, created = DailyExpertStats.objects.get_or_create(
        expert=expert,
        date=timezone.now().date(),
        defaults={'sessions_count': 1, 'revenue': revenue},
    )
    if not created:
        expert_stats_obj.sessions_count += 1
        expert_stats_obj.revenue += float(revenue)
        expert_stats_obj.save()


@shared_task
def calculate_expert_average_rating(expert_id, new_rating):
    """
    Task to calculate expert's average rating.
    """
    expert = Expert.objects.get(userbase=expert_id)

    total_rating = expert.avg_rating * expert.num_rating
    expert.avg_rating = (total_rating + new_rating) / (expert.num_rating + 1)
    expert.num_rating += 1
    expert.save()


@shared_task
def apply_payments_for_completed_session(session_id, total_amount):
    """
    Task to deduct amount from card for a completed session.
    """
    SessionTransaction = apps.get_model('experchat_sessions', 'SessionTransaction')
    transactions = SessionTransaction.objects.filter(session_id=session_id, transaction__status=Transaction.UNSETTLED)
    amount_sum = 0
    for session_transaction in transactions:
        if session_transaction.transaction.promo_code:
            session_transaction.transaction.status = Transaction.SETTLED
            session_transaction.transaction.save()
        else:
            amount_sum += int(session_transaction.transaction.amount)
            if amount_sum <= int(total_amount):
                ExperchatPayment().settle_transaction(transaction=session_transaction.transaction,
                                                      amount=session_transaction.transaction.amount)
            else:
                ExperchatPayment().cancel_transaction(transaction=session_transaction.transaction)


@shared_task
def cancel_payment_on_session_cancellation(session_id):
    Session = apps.get_model('experchat_sessions', 'Session')
    session = Session.objects.get(id=session_id)
    SessionTransaction = apps.get_model('experchat_sessions', 'SessionTransaction')
    transactions = SessionTransaction.objects.filter(session_id=session_id, transaction__status=Transaction.UNSETTLED)

    time_after_two_hour_of_scheduling = (
        session.created_timestamp + timezone.timedelta(hours=settings.NO_CANCELLATION_CHARGES_POST_SCHEDULE_DURATION)
    )
    time_before_24_hours_of_scheduled_datetime = (
        session.scheduled_datetime -
        timezone.timedelta(hours=settings.NO_CANCELLATION_CHARGES_PRIOR_APPOINTMENT_DURATION)
    )

    if (
        timezone.now() <= time_after_two_hour_of_scheduling or
        timezone.now() <= time_before_24_hours_of_scheduled_datetime
            ):
        for session_transaction in transactions:
            if session_transaction.transaction.promo_code:
                session_transaction.transaction.status = Transaction.CANCELLED
                session_transaction.transaction.save()
            else:
                ExperchatPayment().cancel_transaction(transaction=session_transaction.transaction)

    else:  # Deduct cancellation charges
        for session_transaction in transactions:
            if session_transaction.transaction.promo_code:
                session_transaction.transaction.status = Transaction.CANCELLED
                session_transaction.transaction.save()
            else:
                cancellation_amount = (
                    float(session_transaction.transaction.amount) * settings.SESSION_CANCELLATION_PERCENTAGE_AMOUNT/100
                )
                ExperchatPayment().settle_transaction(transaction=session_transaction.transaction,
                                                      amount=str(cancellation_amount))


@shared_task
def cancel_payment_on_user_missed(session_id):
    Session = apps.get_model('experchat_sessions', 'Session')
    session = Session.objects.get(id=session_id)
    SessionTransaction = apps.get_model('experchat_sessions', 'SessionTransaction')
    transactions = SessionTransaction.objects.filter(session_id=session_id, transaction__status=Transaction.UNSETTLED)

    if session.call_status == CallStatus.SCHEDULED.value:
        for session_transaction in transactions:
            if session_transaction.transaction.promo_code:
                session_transaction.transaction.status = Transaction.CANCELLED
                session_transaction.transaction.save()
            else:
                cancellation_amount = (
                    float(session_transaction.transaction.amount) * settings.SESSION_CANCELLATION_PERCENTAGE_AMOUNT/100
                )
                ExperchatPayment().settle_transaction(transaction=session_transaction.transaction,
                                                      amount=str(cancellation_amount))


@shared_task
def apply_payments_for_all_completed_session():
    """
    Task to deduct amount from card for all the completed session.
    """
    Session = apps.get_model('experchat_sessions', 'Session')
    sessions = Session.objects.filter(
        call_status=CallStatus.COMPLETED,
        sessiontransaction__transaction__status=Transaction.UNSETTLED
    ).prefetch_related('sessiontransaction_set__transaction')

    for session in sessions:
        transactions = session.sessiontransaction_set.all()
        amount_sum = 0
        for session_transaction in transactions:
            if session_transaction.transaction.promo_code:
                session_transaction.transaction.status = Transaction.SETTLED
                session_transaction.transaction.save()
            else:
                amount_sum += int(session_transaction.transaction.amount)
                if amount_sum <= int(session.revenue):
                    ExperchatPayment().settle_transaction(transaction=session_transaction.transaction,
                                                          amount=session_transaction.transaction.amount)
                else:
                    ExperchatPayment().cancel_transaction(transaction=session_transaction.transaction)
