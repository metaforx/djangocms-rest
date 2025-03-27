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

    def test_rendering_languages(self):
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

        result = self.client.get(reverse("language-list"))
        self.assertEqual(result.status_code, 200)
        data = {item["code"]: item for item in result.json()}

        for lang_config in languages:
            lang = lang_config["code"]

            # Type validation
            for item in check_items:
                self.assertEqual(lang_config[item], data[lang][item])
                self.assertIsInstance(data[lang][item], type_checks[item],f"Field '{item}' should be of type {type_checks[item].__name__}")

                # Check list element types
                if item == "fallbacks":
                    for fallback in data[lang][item]:
                        self.assertIsInstance(fallback, str,"Fallback language codes should be strings")
                        self.assertLessEqual(len(fallback), 4,"Fallback language code should not exceed 4 characters")
