from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.utils import assert_field_types


class PageRootAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the page root endpoint ('/api/{language}/pages-root/').

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
        response = self.client.get(reverse("page-root", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
        page = response.json()

        #Data & Type Validation
        for field, expected_type in type_checks.items():
            self.assertIn(field, page, f"Field {field} is missing")

            if isinstance(expected_type, tuple):
                assert_field_types(
                    self,
                    page,
                    field,
                    expected_type,
                )

        # Check Invalid Language
        response = self.client.get(reverse("page-root", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)

        # GET PREVIEW
        response = self.client.get(reverse("preview-page-root", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("preview-page-root", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preview-page-root", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
