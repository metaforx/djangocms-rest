from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from django.urls import reverse


class RESTTestCase(CMSTestCase):
    prefix = "http://testserver"


class RenderingTestCase(RESTTestCase):
    def _create_pages(self, page_list, parent=None):
        new_pages =  [create_page(
            f"page {i}",
            language="en",
            template="INHERIT",
            parent=parent
        ) for i in range(page_list if isinstance(page_list, int) else len(page_list))]
        if isinstance(page_list, list):
            for i, page in enumerate(new_pages):
                self._create_pages(page_list[i], page)
        else:
            self.pages = new_pages

    def setUp(self):
        self._create_pages([2, (3, 1), 2])

    def test_endpoint_languages(self):
        """
        Test the languages endpoint (/api/languages/).

        Verifies:
        - Endpoint returns correct HTTP status code
        - Response contains all required language fields
        - All fields have correct data types
        - Language codes match CMS settings
        """

        from cms.utils.conf import get_cms_setting

        languages = get_cms_setting("LANGUAGES")[1]
        check_items = (
            "code",
            "name",
            "public",
            "redirect_on_fallback",
            "fallbacks",
            "hide_untranslated"
        )

        type_checks = {
            "code": str,
            "name": str,
            "public": bool,
            "redirect_on_fallback": bool,
            "fallbacks": list,
            "hide_untranslated": bool
        }

        # Request/Response
        response = self.client.get(reverse("language-list"))
        self.assertEqual(response.status_code, 200)
        data = {item["code"]: item for item in response.json()}

        for lang_config in languages:
            lang = lang_config["code"]

            # Data & Type Validation
            for item in check_items:
                self.assertEqual(lang_config[item], data[lang][item])
                self.assertIsInstance(data[lang][item], type_checks[item],f"Field '{item}' should be of type {type_checks[item].__name__}")

                # Nested Data & Type Validation
                if item == "fallbacks":
                    for fallback in data[lang][item]:
                        self.assertIsInstance(fallback, str,"Fallback language codes should be strings")
                        self.assertLessEqual(len(fallback), 4,"Fallback language code should not exceed 4 characters")

    def test_endpoint_page_tree_list(self):
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
            "children"
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
            "children": list
        }

        # Request/Response
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
                        f"Field {field} should be one of types {expected_type}, got {type(page[field])}"
                    )
                else:
                    self.assertIsInstance(
                        page[field],
                        expected_type,
                        f"Field {field} should be {expected_type}, got {type(page[field])}"
                    )

            # Nested Data & Type Validation
            for child in page['children']:
                for field, expected_type in type_checks.items():
                    self.assertIn(field, child)
                    if isinstance(expected_type, tuple):
                        self.assertTrue(isinstance(child[field], expected_type))
                    else:
                        self.assertIsInstance(child[field], expected_type)

        # Check Invalid Language
        response = self.client.get(reverse("page-tree-list", kwargs={"language": "xx"}))
        self.assertEqual(response.status_code, 404)
