from django.test import TestCase, Client

# Create your tests here.
req_test_health = {}

class HealthTest(TestCase):

    def test_healt(self):

        response = Client().get('/health',req_test_health)
        self.assertEqual(response.status_code,200)