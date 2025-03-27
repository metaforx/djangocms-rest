from django.urls import reverse

from tests.base import BaseCMSRestTestCase


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

        check_items = (
            "title",
            "page_title",
            "menu_title",
            "meta_description",
            "redirect",
            "in_navigation",
            "soft_root",
            "template",
            "xframe_options",
            "limit_visibility_in_menu",
            "language",
            "path",
            "absolute_url",
            "is_home",
            "languages",
            "is_preview",
            "creation_date",
            "changed_date",
            "children",
        )

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
        tree_data = response.json()

        # Data & Type Validation
        self.assertIsInstance(tree_data, list)
        for page in tree_data:
            for item in check_items:
                self.assertIn(item, page, f"Field {item} is missing")

            for field, expected_type in type_checks.items():
                if isinstance(expected_type, tuple):
                    self.assertTrue(
                        isinstance(page[field], expected_type),
                        f"Field {field} should be one of types {expected_type}, got {type(page[field])}",
                    )
                else:
                    self.assertIsInstance(
                        page[field],
                        expected_type,
                        f"Field {field} should be {expected_type}, got {type(page[field])}",
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
