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
        self.assertEqual(response.data.get("p1_life"), 40)
        self.assertEqual(response.data.get("p2_life"), 40)

        ## Implementation Testing (White Box)
        self.assertTrue(
            LifeCounter.objects.exists(),
            "Life Counter object should be created upon calling the url when no life counter object exists",
        )
        with self.subTest("Test for existing life counter"):
            LifeCounter.objects.update(p1_life=20, p2_life=30)

            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get("p1_life"), 20)
            self.assertEqual(response.data.get("p2_life"), 30)

            self.assertEqual(1, LifeCounter.objects.count())

    def test_reset(self):
        """
        Expected Behavior:
            When POST /life_counter/reset/ is called, Life counter is set back to 40 for both players
        """
        url = f"{self.url}reset/"
        response = self.client.post(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data.get("p1_life"), 40)
        self.assertEqual(response.data.get("p2_life"), 40)

        self.assertEqual(LifeCounter.objects.first().p1_life, 40)
        self.assertEqual(LifeCounter.objects.first().p2_life, 40)

    def test_patch(self):
        """
        Expected Request Body:
            url: PATCH /life_counter/<player_number: p1 or p2>/increment/
            or
            url: PATCH /life_counter/<player_number>/decrement/
        """
