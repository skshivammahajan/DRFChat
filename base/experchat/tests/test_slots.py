from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from experchat.models.appointments import Calendar, WeekDay
from experchat.models.domains import Domain, Tag
from experchat.models.session_pricing import SessionPricing
from experchat.models.sessions import EcDevice, EcSession
from experchat.models.users import Expert, ExpertProfile
from experchat.utils import (
    combine_slots, filter_slots, get_booked_and_available_slots, get_slot_datetime, process_and_merge_slots,
    split_and_update_price, split_in_duration
)

User = get_user_model()


@pytest.mark.django_db
class TestSlotsFeature(TestCase):
    """
    Test case for testing the utils for merging and making the next 3 months slots
    """
    def setUp(self):
        # make the date for testing
        self.today_for_next = get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                timezone.pytz.UTC)
        self.time = get_slot_datetime(timezone.datetime.strptime('2017-04-04', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('2:30', "%H:%M").time(),
                                                timezone.pytz.UTC)

        self.today_date = timezone.datetime.strptime('2017-04-04', "%Y-%m-%d")
        # expected valid merged slots
        self.expected_merged_slots = [
            {
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('5:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                timezone.pytz.UTC)
            },
            {
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('12:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC)
            },
            {
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('5:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('14:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 5,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-07', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('15:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-07', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-07', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('5:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('12:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('5:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('14:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            },
            {
                'day': 5,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-14', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('15:30', "%H:%M").time(),
                                              timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-14', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-14', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
            }
        ]

        self.user = User.objects.create(email='testuser@example.com', is_email_verified=True)
        self.expert = Expert.objects.create(userbase=self.user)
        self.domain = Domain.objects.create(name='Test Case Creation')
        self.tag = Tag.objects.create(domain=self.domain, name='Hairstyles')
        self.expert_profile = ExpertProfile.objects.create(expert=self.expert)
        self.user_device = EcDevice.objects.create(user=self.user)

        for day in [1, 2, 3, 4, 5, 6, 7]:
            WeekDay.objects.create(day=day)

        # test data for creating the calendar
        test_data_for_available_slots = [
            {
                'start_time': '04:40',
                'end_time': '05:30',
                'days': [3, 4],
                'title': 'First Slots'
            },
            {
                'start_time': '10:40',
                'end_time': '11:30',
                'days': [3, 4],
                'title': 'Second Slots'
            },
            {
                'start_time': '10:40',
                'end_time': '11:30',
                'days': [5],
                'title': 'Third Slots'
            },
            {
                'start_time': '10:50',
                'end_time': '12:30',
                'days': [3, 4, 5],
                'title': 'Fourth Slots'
            },
            {
                'start_time': '10:55',
                'end_time': '14:30',
                'days': [4, 5],
                'title': 'Fifth Slots'
            },
            {
                'start_time': '12:55',
                'end_time': '15:30',
                'days': [5],
                'title': 'Sixth Slots'
            }
        ]

        test_data_for_booked_slots = [
            {
                'scheduled_duration': 10,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 20,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 20,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('12:00', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 20,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 30,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 10,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:50', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 60,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:00', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 30,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:00', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 20,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'scheduled_duration': 20,
                'scheduled_datetime': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
        ]

        self.expected_booked_slots = [
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('5:10', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'date_string':  timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'date_string':  timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('12:00', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('12:20', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'date_string':  timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string':  timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:30', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string':  timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:30', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:50', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date()
            },
            {
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'date_string': timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date()
            }
        ]

        # creating the calendar
        for data in test_data_for_available_slots:
            calendar = Calendar.objects.create(
                title=data['title'],
                expert=self.expert,
                start_time=data['start_time'],
                end_time=data['end_time'],
                timezone='UTC'
            )
            calendar.week_days = data['days']
            calendar.save()

        for data in test_data_for_booked_slots:
            EcSession.objects.create(
                expert_profile=self.expert_profile,
                expert=self.expert,
                user=self.user,
                user_device=self.user_device,
                tokbox_session_id=1020,
                tokbox_session_length=30,
                revenue=40,
                call_status=6,
                scheduled_duration=data['scheduled_duration'],
                scheduled_datetime=data['scheduled_datetime']
            )

        # all available slots
        self.available_slots = Calendar.objects.filter(expert__userbase=self.expert.id).order_by('start_time')
        self.expected_filtered_slots_result = [
            {
                'date_string': timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('5:00', "%H:%M").time(),
                                              timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('5:10', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('5:30', "%H:%M").time(),
                                              timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                                timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                timezone.pytz.UTC),
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date(),
                                              timezone.datetime.strptime('12:00', "%H:%M").time(),
                                              timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-06', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('14:30', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-07', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-07', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 5,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-07', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('15:30', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('4:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:30', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 3,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-12', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('12:30', "%H:%M").time(),
                                                        timezone.pytz.UTC),
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('5:30', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('11:00', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 4,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-13', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('14:30', "%H:%M").time(),
                                                        timezone.pytz.UTC),
            },
            {
                'date_string': timezone.datetime.strptime('2017-04-14', "%Y-%m-%d").date(),
                'start_time': get_slot_datetime(timezone.datetime.strptime('2017-04-14', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('10:40', "%H:%M").time(),
                                                        timezone.pytz.UTC),
                'day': 5,
                'end_time': get_slot_datetime(timezone.datetime.strptime('2017-04-14', "%Y-%m-%d").date(),
                                                        timezone.datetime.strptime('15:30', "%H:%M").time(),
                                                        timezone.pytz.UTC)
            }
        ]

        self.spected_splited_slots_in_10_default_tz = {
            10: {
                '2017-04-07':[
                    {'start_time': '10:40'}, {'start_time': '10:50'}, {'start_time': '11:00'}, {'start_time': '11:10'},
                    {'start_time': '11:20'}, {'start_time': '11:30'}, {'start_time': '11:40'}, {'start_time': '11:50'},
                    {'start_time': '12:00'}, {'start_time': '12:10'}, {'start_time': '12:20'}, {'start_time': '12:30'},
                    {'start_time': '12:40'}, {'start_time': '12:50'}, {'start_time': '13:00'}, {'start_time': '13:10'},
                    {'start_time': '13:20'}, {'start_time': '13:30'}, {'start_time': '13:40'}, {'start_time': '13:50'},
                    {'start_time': '14:00'}, {'start_time': '14:10'}, {'start_time': '14:20'}, {'start_time': '14:30'},
                    {'start_time': '14:40'}, {'start_time': '14:50'}, {'start_time': '15:00'}, {'start_time': '15:10'},
                    {'start_time': '15:20'}
                ],
                '2017-04-14': [
                    {'start_time': '10:40'}, {'start_time': '10:50'}, {'start_time': '11:00'}, {'start_time': '11:10'},
                    {'start_time': '11:20'}, {'start_time': '11:30'}, {'start_time': '11:40'}, {'start_time': '11:50'},
                    {'start_time': '12:00'}, {'start_time': '12:10'}, {'start_time': '12:20'}, {'start_time': '12:30'},
                    {'start_time': '12:40'}, {'start_time': '12:50'}, {'start_time': '13:00'}, {'start_time': '13:10'},
                    {'start_time': '13:20'}, {'start_time': '13:30'}, {'start_time': '13:40'}, {'start_time': '13:50'},
                    {'start_time': '14:00'}, {'start_time': '14:10'}, {'start_time': '14:20'}, {'start_time': '14:30'},
                    {'start_time': '14:40'}, {'start_time': '14:50'}, {'start_time': '15:00'}, {'start_time': '15:10'},
                    {'start_time': '15:20'}
                ],
                '2017-04-05': [
                    {'start_time': '04:40'}, {'start_time': '04:50'}, {'start_time': '05:10'}, {'start_time': '05:20'},
                    {'start_time': '11:00'}, {'start_time': '11:10'}, {'start_time': '11:20'},
                    {'start_time': '11:30'}, {'start_time': '11:40'}, {'start_time': '11:50'}
                ],
                '2017-04-06': [
                    {'start_time': '11:00'}, {'start_time': '11:10'}, {'start_time': '11:20'}, {'start_time': '11:30'},
                    {'start_time': '11:40'}, {'start_time': '11:50'}, {'start_time': '12:00'}, {'start_time': '12:10'},
                    {'start_time': '12:20'}, {'start_time': '12:30'}, {'start_time': '12:40'}, {'start_time': '12:50'},
                    {'start_time': '13:00'}, {'start_time': '13:10'}, {'start_time': '13:20'}, {'start_time': '13:30'},
                    {'start_time': '13:40'}, {'start_time': '13:50'}, {'start_time': '14:00'}, {'start_time': '14:10'},
                    {'start_time': '14:20'}
                ],
                '2017-04-13': [
                    {'start_time': '05:00'}, {'start_time': '05:10'}, {'start_time': '05:20'}, {'start_time': '11:00'},
                    {'start_time': '11:10'}, {'start_time': '11:20'}, {'start_time': '11:30'}, {'start_time': '11:40'},
                    {'start_time': '11:50'}, {'start_time': '12:00'}, {'start_time': '12:10'}, {'start_time': '12:20'},
                    {'start_time': '12:30'}, {'start_time': '12:40'}, {'start_time': '12:50'}, {'start_time': '13:00'},
                    {'start_time': '13:10'}, {'start_time': '13:20'}, {'start_time': '13:30'}, {'start_time': '13:40'},
                    {'start_time': '13:50'}, {'start_time': '14:00'}, {'start_time': '14:10'}, {'start_time': '14:20'}
                ],
                '2017-04-12': [
                    {'start_time': '04:40'}, {'start_time': '04:50'}, {'start_time': '05:00'}, {'start_time': '05:10'},
                    {'start_time': '05:20'}, {'start_time': '10:40'}, {'start_time': '10:50'}, {'start_time': '11:00'},
                    {'start_time': '11:10'}, {'start_time': '11:20'}, {'start_time': '11:30'}, {'start_time': '11:40'},
                    {'start_time': '11:50'}, {'start_time': '12:00'}, {'start_time': '12:10'}, {'start_time': '12:20'}
                ]
            }
        }

        self.spected_splited_slots_in_20_default_tz = {
            20: {
                '2017-04-14': [
                    {'start_time': '10:40'}, {'start_time': '11:00'}, {'start_time': '11:20'}, {'start_time': '11:40'},
                    {'start_time': '12:00'}, {'start_time': '12:20'}, {'start_time': '12:40'}, {'start_time': '13:00'},
                    {'start_time': '13:20'}, {'start_time': '13:40'}, {'start_time': '14:00'}, {'start_time': '14:20'},
                    {'start_time': '14:40'}, {'start_time': '15:00'}
                ],
                '2017-04-12': [
                    {'start_time': '04:40'}, {'start_time': '05:00'}, {'start_time': '10:40'}, {'start_time': '11:00'},
                    {'start_time': '11:20'}, {'start_time': '11:40'}, {'start_time': '12:00'}
                ],
                '2017-04-07': [
                    {'start_time': '10:40'}, {'start_time': '11:00'}, {'start_time': '11:20'}, {'start_time': '11:40'},
                    {'start_time': '12:00'}, {'start_time': '12:20'}, {'start_time': '12:40'}, {'start_time': '13:00'},
                    {'start_time': '13:20'}, {'start_time': '13:40'}, {'start_time': '14:00'}, {'start_time': '14:20'},
                    {'start_time': '14:40'}, {'start_time': '15:00'}
                ],
                '2017-04-05': [
                    {'start_time': '04:40'}, {'start_time': '11:00'},
                    {'start_time': '11:20'}, {'start_time': '11:40'}
                ],
                '2017-04-06': [
                    {'start_time': '11:00'}, {'start_time': '11:20'}, {'start_time': '11:40'}, {'start_time': '12:00'},
                    {'start_time': '12:20'}, {'start_time': '12:40'}, {'start_time': '13:00'}, {'start_time': '13:20'},
                    {'start_time': '13:40'}, {'start_time': '14:00'}
                ],
                '2017-04-13': [
                    {'start_time': '05:00'}, {'start_time': '11:00'}, {'start_time': '11:20'}, {'start_time': '11:40'},
                    {'start_time': '12:00'}, {'start_time': '12:20'}, {'start_time': '12:40'}, {'start_time': '13:00'},
                    {'start_time': '13:20'}, {'start_time': '13:40'}, {'start_time': '14:00'}
                ]
            }
        }

        self.spected_splited_slots_in_30_default_tz = {
            30: {
                '2017-04-14': [
                    {'start_time': '11:00'}, {'start_time': '11:30'}, {'start_time': '12:00'}, {'start_time': '12:30'},
                    {'start_time': '13:00'}, {'start_time': '13:30'}, {'start_time': '14:00'}, {'start_time': '14:30'},
                    {'start_time': '15:00'}
                ],
                '2017-04-06': [
                    {'start_time': '11:00'}, {'start_time': '11:30'}, {'start_time': '12:00'}, {'start_time': '12:30'},
                    {'start_time': '13:00'}, {'start_time': '13:30'}, {'start_time': '14:00'}
                ],
                '2017-04-12': [
                    {'start_time': '05:00'}, {'start_time': '11:00'}, {'start_time': '11:30'}, {'start_time': '12:00'}
                ],
                '2017-04-05': [
                    {'start_time': '11:00'}, {'start_time': '11:30'}
                ],
                '2017-04-07': [
                    {'start_time': '11:00'}, {'start_time': '11:30'}, {'start_time': '12:00'}, {'start_time': '12:30'},
                    {'start_time': '13:00'}, {'start_time': '13:30'}, {'start_time': '14:00'}, {'start_time': '14:30'},
                    {'start_time': '15:00'}
                ],
                '2017-04-13': [
                    {'start_time': '05:00'}, {'start_time': '11:00'}, {'start_time': '11:30'}, {'start_time': '12:00'},
                    {'start_time': '12:30'}, {'start_time': '13:00'}, {'start_time': '13:30'}, {'start_time': '14:00'}
                ]
            }
        }
        self.spected_splited_slots_in_60_default_tz = {
            60: {
                '2017-04-14': [
                    {'start_time': '11:00'}, {'start_time': '12:00'}, {'start_time': '13:00'}, {'start_time': '14:00'}                ],
                '2017-04-06': [
                    {'start_time': '11:00'}, {'start_time': '12:00'}, {'start_time': '13:00'}
                ],
                '2017-04-12': [
                    {'start_time': '11:00'}
                ],
                '2017-04-05': [
                    {'start_time': '11:00'}
                ],
                '2017-04-07': [
                    {'start_time': '11:00'}, {'start_time': '12:00'}, {'start_time': '13:00'}, {'start_time': '14:00'}
                ],
                '2017-04-13': [
                    {'start_time': '11:00'}, {'start_time': '12:00'}, {'start_time': '13:00'}
                ]
            }
        }

        self.session_pricing_data = [
            {'session_length': 10, 'price': 20},
            {'session_length': 20, 'price': 40},
            {'session_length': 30, 'price': 50},
            {'session_length': 60, 'price': 70}
        ]
        for data in self.session_pricing_data:
            SessionPricing.objects.create(
                session_length=data['session_length'],
                price=data['price']
            )

        self.session_pricess = SessionPricing.objects.all()
        self.expected_split_and_update_price = [
            self.spected_splited_slots_in_10_default_tz,
            self.spected_splited_slots_in_20_default_tz,
            self.spected_splited_slots_in_30_default_tz,
            self.spected_splited_slots_in_60_default_tz,
        ]

        self.expected_result_in_indian_timezone_for_split_and_update_price = [{
            10: {
                '2017-04-07': [{
                    'start_time': '16:10'
                }, {
                    'start_time': '16:20'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '16:50'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:10'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '17:50'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:10'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '18:50'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:10'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:30'
                }, {
                    'start_time': '19:40'
                }, {
                    'start_time': '19:50'
                }, {
                    'start_time': '20:00'
                }, {
                    'start_time': '20:10'
                }, {
                    'start_time': '20:20'
                }, {
                    'start_time': '20:30'
                }, {
                    'start_time': '20:40'
                }, {
                    'start_time': '20:50'
                }],
                '2017-04-12': [{
                    'start_time': '10:10'
                }, {
                    'start_time': '10:20'
                }, {
                    'start_time': '10:30'
                }, {
                    'start_time': '10:40'
                }, {
                    'start_time': '10:50'
                }, {
                    'start_time': '16:10'
                }, {
                    'start_time': '16:20'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '16:50'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:10'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '17:50'
                }],
                '2017-04-14': [{
                    'start_time': '16:10'
                }, {
                    'start_time': '16:20'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '16:50'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:10'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '17:50'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:10'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '18:50'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:10'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:30'
                }, {
                    'start_time': '19:40'
                }, {
                    'start_time': '19:50'
                }, {
                    'start_time': '20:00'
                }, {
                    'start_time': '20:10'
                }, {
                    'start_time': '20:20'
                }, {
                    'start_time': '20:30'
                }, {
                    'start_time': '20:40'
                }, {
                    'start_time': '20:50'
                }],
                '2017-04-06': [{
                    'start_time': '16:30'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '16:50'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:10'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '17:50'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:10'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '18:50'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:10'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:30'
                }, {
                    'start_time': '19:40'
                }, {
                    'start_time': '19:50'
                }],
                '2017-04-05':[{
                    'start_time': '10:10'
                }, {
                    'start_time': '10:20'
                }, {
                    'start_time': '10:40'
                }, {
                    'start_time': '10:50'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '16:50'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:10'
                }, {
                    'start_time': '17:20'
                }],
                '2017-04-13': [{
                    'start_time': '10:30'
                }, {
                    'start_time': '10:40'
                }, {
                    'start_time': '10:50'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '16:50'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:10'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '17:50'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:10'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '18:50'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:10'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:30'
                }, {
                    'start_time': '19:40'
                }, {
                    'start_time': '19:50'
                }]
            }
        }, {
            20: {
                '2017-04-05': [{
                    'start_time': '10:40'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '17:00'
                }],
                '2017-04-07': [{
                    'start_time': '16:20'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:40'
                }, {
                    'start_time': '20:00'
                }, {
                    'start_time': '20:20'
                }, {
                    'start_time': '20:40'
                }],
                '2017-04-12': [{
                    'start_time': '10:20'
                }, {
                    'start_time': '10:40'
                }, {
                    'start_time': '16:20'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:40'
                }],
                '2017-04-14': [{
                    'start_time': '16:20'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:40'
                }, {
                    'start_time': '20:00'
                }, {
                    'start_time': '20:20'
                }, {
                    'start_time': '20:40'
                }],
                '2017-04-06': [{
                    'start_time': '16:40'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:40'
                }],
                '2017-04-13': [{
                    'start_time': '10:40'
                }, {
                    'start_time': '16:40'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:20'
                }, {
                    'start_time': '17:40'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:20'
                }, {
                    'start_time': '18:40'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:20'
                }, {
                    'start_time': '19:40'
                }]
            }
        }, {
            30: {
                '2017-04-05': [{
                    'start_time': '16:30'
                }, {
                    'start_time': '17:00'
                }],
                '2017-04-07': [{
                    'start_time': '16:30'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:30'
                }, {
                    'start_time': '20:00'
                }, {
                    'start_time': '20:30'
                }],
                '2017-04-12': [{
                    'start_time': '10:30'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:30'
                }],
                '2017-04-14': [{
                    'start_time': '16:30'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:30'
                }, {
                    'start_time': '20:00'
                }, {
                    'start_time': '20:30'
                }],
                '2017-04-06': [{
                    'start_time': '16:30'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:30'
                }],
                '2017-04-13': [{
                    'start_time': '10:30'
                }, {
                    'start_time': '16:30'
                }, {
                    'start_time': '17:00'
                }, {
                    'start_time': '17:30'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '18:30'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '19:30'
                }]
            }
        }, {
            60: {
                '2017-04-07': [{
                    'start_time': '17:00'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '20:00'
                }],
                '2017-04-12': [{
                    'start_time': '17:00'
                }],
                '2017-04-14': [{
                    'start_time': '17:00'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '19:00'
                }, {
                    'start_time': '20:00'
                }],
                '2017-04-06': [{
                    'start_time': '17:00'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '19:00'
                }],
                '2017-04-13': [{
                    'start_time': '17:00'
                }, {
                    'start_time': '18:00'
                }, {
                    'start_time': '19:00'
                }]
            }}]

        self.expected_next_day_response = [
            timezone.datetime.strptime('2017-04-06' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '12:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '13:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '13:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '14:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '12:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '13:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '13:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '14:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '14:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '15:00', '%Y-%m-%dT%H:%M'),
        ]

        self.expected_all_day_results = [
            timezone.datetime.strptime('2017-04-05' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-05' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '12:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '13:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '13:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-06' + 'T' + '14:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '12:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '13:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '13:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '14:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '14:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-07' + 'T' + '15:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-12' + 'T' + '5:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-12' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-12' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-12' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '5:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '12:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '13:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '13:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-13' + 'T' + '14:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '11:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '11:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '12:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '12:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '13:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '13:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '14:00', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '14:30', '%Y-%m-%dT%H:%M'),
            timezone.datetime.strptime('2017-04-14' + 'T' + '15:00', '%Y-%m-%dT%H:%M')
        ]

    def test_process_and_merge_slots_valid(self):
        """
        test case for merged slots with valid expected result
        """
        merge_slots = process_and_merge_slots(self.available_slots, today=self.today_date)
        assert merge_slots == self.expected_merged_slots

    def test_process_and_merge_slots_valid_without_slots(self):
        """
        test case for merged slots with valid expected result without any slots
        """
        slots = Calendar.objects.filter(expert__userbase=2).order_by('start_time')
        merge_slots = process_and_merge_slots(slots, today=self.today_date)
        assert merge_slots == []

    def test_get_slot_datetime_utc(self):
        """
        test case for get_slot_datetime when timezone is Asia/Kolkata
        """
        date = timezone.datetime.strptime('2017-04-05', "%Y-%m-%d").date()
        time = timezone.datetime.strptime('5:30', "%H:%M").time()
        result = get_slot_datetime(date, time, 'Asia/Kolkata')
        datetime = timezone.datetime.strptime('2017-04-05 5:30', "%Y-%m-%d %H:%M")
        expected_result = timezone.make_aware(datetime, timezone.pytz.timezone('Asia/Kolkata')).astimezone(timezone.pytz.UTC)
        assert result == expected_result

    def test_get_booked_and_available_slots(self):
        """
        test case for geting the booked and available slots
        """
        available_slots, booked_slots = get_booked_and_available_slots(self.expert.id)
        assert booked_slots == self.expected_booked_slots

    @mock.patch('experchat.utils.process_and_merge_slots')
    def test_filter_slots_with_both_data_available(self, mock_process_and_merge_slots):
        """
        Test case for filter_slots when booked slots and available sots are there
        """
        mock_process_and_merge_slots.return_value = self.expected_merged_slots
        result = filter_slots(self.available_slots, self.expected_booked_slots)
        assert result == self.expected_filtered_slots_result

    @mock.patch('experchat.utils.process_and_merge_slots')
    def test_filter_slots_without_booked_slots(self, mock_process_and_merge_slots):
        """
        Test case for filter_slots when booked slots and available sots are there
        """
        mock_process_and_merge_slots.return_value = self.expected_merged_slots
        result = filter_slots(self.available_slots, [])
        assert result == self.expected_merged_slots

    def test_split_in_duration_with_10(self):
        """
        Test case for split_in_duration method with duration as 10 and price as 20 default timezone
        """
        result = split_in_duration(self.expected_filtered_slots_result, 10, price=20, current_time=self.time)
        assert result.keys() == self.spected_splited_slots_in_10_default_tz.keys()
        for key, value in result[10].items():
            assert value == self.spected_splited_slots_in_10_default_tz[10][key]

    def test_split_in_duration_with_20(self):
        """
        Test case for split_in_duration method with duration as 20 and price as 40 default timezone
        """
        result = split_in_duration(self.expected_filtered_slots_result, 20, price=40, current_time=self.time)
        assert result.keys() == self.spected_splited_slots_in_20_default_tz.keys()
        for key, value in result[20].items():
            assert value ==  self.spected_splited_slots_in_20_default_tz[20][key]

    def test_split_in_duration_with_30(self):
        """
        Test case for split_in_duration method with duration as 30 and price as 50 default timezone
        """
        result = split_in_duration(self.expected_filtered_slots_result, 30, price=50, current_time=self.time)
        assert result.keys() == self.spected_splited_slots_in_30_default_tz.keys()
        for key, value in result[30].items():
            assert value ==  self.spected_splited_slots_in_30_default_tz[30][key]

    def test_split_in_duration_with_60(self):
        """
        Test case for split_in_duration method with duration as 60 and price as 70 default timezone
        """
        result = split_in_duration(self.expected_filtered_slots_result, 60, price=70, current_time=self.time)
        assert result.keys() == self.spected_splited_slots_in_60_default_tz.keys()
        for key, value in result[60].items():
            assert value ==  self.spected_splited_slots_in_60_default_tz[60][key]

    def test_split_in_duration_without_slots(self):
        """
        Test case for split_in_duration method without any slots
        """
        result = split_in_duration([], 60, price=70, current_time=self.time)
        assert result == []

    def test_split_and_update_price_with_defalut_timezone(self):
        """
        test split_and_update_price with default timezone
        """
        result = split_and_update_price(self.expected_filtered_slots_result, current_time=self.time)
        assert result == self.expected_split_and_update_price

    def test_split_and_update_price_with_india_timezone(self):
        """
        test split_and_update_price with Asia/Kolkata
        """
        result = split_and_update_price(self.expected_filtered_slots_result, time_zone='Asia/Kolkata',
                                        current_time=self.time)
        assert result == self.expected_result_in_indian_timezone_for_split_and_update_price

    def test_combine_slots_for_next_day_only(self):
        """
        test case for combine_slots when we need slots data only for today and nextday
        """
        result = combine_slots(self.spected_splited_slots_in_30_default_tz, only_till_next_day=True,
                               today=self.today_for_next)
        assert result == self.expected_next_day_response

    def test_combine_slots_for_next_day_only_without_slots(self):
        """
        test case for combine_slots when no slots provided
        """
        result = combine_slots([], only_till_next_day=True)
        assert result == []

    def test_combine_slots_for_all_days(self):
        """
        test case for combine_slots for detail API where we need to display all slots
        """
        result = combine_slots(self.spected_splited_slots_in_30_default_tz, today=self.time)
        assert result == self.expected_all_day_results
