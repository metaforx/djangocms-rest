from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase


class HealthCheckAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the healthcheck endpoint (/api/healthcheck/).

        Verifies:
        - Endpoint returns 200 OK
        - Response contains status field with value "ok"
        """

        # GET
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data, {"status": "ok"})
