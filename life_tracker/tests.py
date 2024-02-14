from rest_framework.test import APITestCase

from .models import LifeCounter

# Create your tests here.


class LifeTrackerTestCase(APITestCase):
    def setUp(self):
        self.url = "/life_counter/"
        LifeCounter.objects.all().delete()

    def test_get(self):
        """
        Expected Behavior:
            when GET /life_counter/ is called, get the life totals of the two players, if the game just started, life should be 40,40
        """
        # No life counter object exists
        response = self.client.get(self.url)
        ## Functionality Testing (Black box)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("p1"), 40)
        self.assertEqual(response.data.get("p2"), 40)

        ## Implementation Testing (White Box)
        self.assertTrue(
            LifeCounter.objects.exists(),
            "Life Counter object should be created upon calling the url when no life counter object exists",
        )
