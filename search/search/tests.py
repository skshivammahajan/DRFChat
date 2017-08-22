from django.contrib.auth import get_user_model
from django.test import TestCase

import pytest
from experchat.models.stats import DailyExpertStats
from experchat.models.users import Expert, ExpertProfile
from search.tasks import calculate_daily_expert_stats

UserBase = get_user_model()


@pytest.mark.django_db
class TestDailyExpertStats(TestCase):
    """
    Test case for Daily Expert Stats.
    """
    def setUp(self):
        """
        SetUp method for test case
        """
        self.u1 = UserBase.objects.create(email='testuser1@example.com', is_email_verified=True)
        self.u2 = UserBase.objects.create(email='testuser2@example.com', is_email_verified=True)
        u3 = UserBase.objects.create(email='testuser3@example.com', is_email_verified=True)
        u4 = UserBase.objects.create(email='testuser4@example.com', is_email_verified=True)
        self.e1 = Expert.objects.create(userbase=u3)
        self.e2 = Expert.objects.create(userbase=u4)
        self.p1 = ExpertProfile.objects.create(expert=self.e1)
        self.p2 = ExpertProfile.objects.create(expert=self.e2)

    def test_calculate_daily_expert_stats_user_one_first_time(self):
        """
        test case for testing Daily Expert Stats
        """
        # First User visiting the expert profile for the first Time
        calculate_daily_expert_stats(self.u1.id, self.p1.id)
        stats_expert_1 = DailyExpertStats.objects.get(expert=self.e1)
        assert stats_expert_1.profile_visits == 1

        # First User visiting the expert profile for the second Time
        calculate_daily_expert_stats(self.u1.id, self.p1.id)
        stats_expert_1 = DailyExpertStats.objects.get(expert=self.e1)
        assert stats_expert_1.profile_visits == 1

        # Second User visiting expert profile for the first Time
        calculate_daily_expert_stats(self.u2.id, self.p1.id)
        stats_expert_1 = DailyExpertStats.objects.get(expert=self.e1)
        assert stats_expert_1.profile_visits == 2

        # Second User visiting expert profile for the second Time
        calculate_daily_expert_stats(self.u2.id, self.p1.id)
        stats_expert_1 = DailyExpertStats.objects.get(expert=self.e1)
        assert stats_expert_1.profile_visits == 2

        # Second User visiting expert profile-2 for the first Time
        calculate_daily_expert_stats(self.u1.id, self.p2.id)
        stats_expert_1 = DailyExpertStats.objects.get(expert=self.e1)
        stats_expert_2 = DailyExpertStats.objects.get(expert=self.e2)
        assert stats_expert_1.profile_visits == 2  # Expert-Profile-1 not visited, so count is same as above
        assert stats_expert_2.profile_visits == 1

        # Second User visiting expert profile-2 for the first Time
        calculate_daily_expert_stats(self.u2.id, self.p2.id)
        stats_expert_1 = DailyExpertStats.objects.get(expert=self.e1)
        stats_expert_2 = DailyExpertStats.objects.get(expert=self.e2)
        assert stats_expert_1.profile_visits == 2  # Expert-Profile-1 not visited, so count is same as above
        assert stats_expert_2.profile_visits == 2
