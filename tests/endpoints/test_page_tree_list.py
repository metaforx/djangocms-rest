from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.utils import assert_field_types


class PageTreeListAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
        """
        Test the page tree list endpoint (/api/{language}/pages-tree/).

        Verifies:
        - Endpoint returns correct HTTP status code
        - Response contains hierarchical page structure
        - All pages contain required fields
        - All fields have correct data types
        - Child pages follow same structure as parent pages
        - Invalid language code returns 404
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
            "children": list,
        }

        # GET
        response = self.client.get(reverse("page-tree-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Data & Type Validation
        self.assertIsInstance(data, list)
        for page in data:
            for field, expected_type in type_checks.items():
                assert_field_types(
                    self,
                    page,
                    field,
                    expected_type,
                )

            # Nested Data & Type Validation
            for child in page["children"]:
                for field, expected_type in type_checks.items():
                    self.assertIn(field, child)
                    if isinstance(expected_type, tuple):
                        self.assertTrue(isinstance(child[field], expected_type))
                    else:
                        self.assertIsInstance(child[field], expected_type)

        # Check Invalid Language
        response = self.client.get(reverse("page-tree-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)

        # GET PREVIEW
        response = self.client.get(reverse("preview-page-tree-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse("preview-page-tree-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 403)

    # GET PREVIEW - Protected
    def test_get_protected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("preview-page-tree-list", kwargs={"language": "en"}))
        self.assertEqual(response.status_code, 200)
