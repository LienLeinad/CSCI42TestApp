from rest_framework.test import APITestCase

# Create your tests here.


class LifeTrackerTestCase(APITestCase):
    def setUp(self):
        url = "/life_tracker/"

    def test_get(self):
        """
        Expected Behavior: when GET /life_tracker/ is called, gets currently cached values of life totals
        Default life total starts at 40
        """
