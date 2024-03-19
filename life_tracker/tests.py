from rest_framework.test import APITestCase

# Create your tests here.
from .models import LifeTracker


class LifeTrackerAPITestCase(APITestCase):
    def test_get_life_tracker(self):
        url = "/life_tracker/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, LifeTracker.objects.count())
        self.assertEqual(40, LifeTracker.objects.first().p1_life)
        self.assertEqual(40, LifeTracker.objects.first().p2_life)
