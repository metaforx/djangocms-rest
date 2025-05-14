from rest_framework.reverse import reverse

from tests.base import BaseCMSRestTestCase
from tests.types import PAGE_TREE_META_FIELD_TYPES
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

        type_checks = PAGE_TREE_META_FIELD_TYPES

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
