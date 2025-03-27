from django.urls import reverse

from tests.base import BaseCMSRestTestCase


class LanguagesAPITestCase(BaseCMSRestTestCase):
    def test_get(self):
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

        # GET
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

