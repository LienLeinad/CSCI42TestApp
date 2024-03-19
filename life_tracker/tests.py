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

    def test_patch_life_totals(self):
        url = "/life_tracker/"

        response = self.client.patch(
            url, {"p1_life": 38, "p2_life": 40, "p1_name": "John", "p2_name": "Doe"}
        )
        self.assertEqual(response.status_code, 201)
        life_tracker = LifeTracker.objects.first()
        self.assertEqual(life_tracker.p1_life, 38)
        self.assertEqual(life_tracker.p2_life, 40)
        self.assertEqual(life_tracker.p1_name, "John")
        self.assertEqual(life_tracker.p2_name, "Doe")

        response = self.client.patch(url, {"p1_life": 40})
        self.assertEqual(response.status_code, 200)
        life_tracker.refresh_from_db()
        self.assertEqual(life_tracker.p1_life, 40)

    def test_reset(self):
        url = "/reset/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 205)
        self.assertFalse(LifeTracker.objects.exists())
