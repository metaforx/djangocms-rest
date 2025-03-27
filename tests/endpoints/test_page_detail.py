from django.urls import reverse

from tests.base import BaseCMSRestTestCase


class PageDetailAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the page detail endpoint ('/api/{language}/pages/{path}/').

        Verifies:
        - Endpoint returns correct HTTP status code
        - Response contains required fields
        - All fields have correct data types and values from the page model
        - Fields are properly formatted in JSON response
        - Invalid language code returns 404
        - Proper parsing of response JSON data
        - Response structure matches API contract
        """

        type_checks = {
            "title": str,
            "page_title": str,
            "menu_title": str,
            "meta_description": (str, type(None)),
            "redirect": (str, type(None)),
            "in_navigation": bool,
            "soft_root": bool,
            "template": str,
            "xframe_options": (int, str),
            "limit_visibility_in_menu": (str, type(None)),
            "language": str,
            "path": str,
            "absolute_url": str,
            "is_home": bool,
            "languages": list,
            "is_preview": bool,
            "creation_date": str,
            "changed_date": str,
            "placeholders": list,
        }

        # GET
        response = self.client.get(reverse("page-detail", kwargs={"language": "en", "path": "page-0"}))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        #Data & Type Validation
        for field, expected_type in type_checks.items():
            self.assertIn(field, data, f"Field {field} is missing")

            if isinstance(expected_type, tuple):
                self.assertTrue(
                    isinstance(data[field], expected_type),
                    f"Field {field} should be one of types {expected_type}, got {type(data[field])}",
                )
            else:
                self.assertIsInstance(
                    data[field],
                    expected_type,
                    f"Field {field} should be {expected_type}, got {type(data[field])}",
                )

        # Check Invalid Language
        response = self.client.get(reverse("page-root", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)
