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
        data = response.json()

        for lang_config in languages:
            lang = lang_config["code"]

            # Data & Type Validation
            for field, expected_type in type_checks.items():
                self.assertEqual(lang_config[field], data[lang][field])
                self.assertIsInstance(data[lang][field], type_checks[field],f"Field '{field}' should be of type {type_checks[field].__name__}")

                # Nested Data & Type Validation
                if field == "fallbacks":
                    for fallback in data[lang][field]:
                        self.assertIsInstance(fallback, str,"Fallback language codes should be strings")
                        self.assertLessEqual(len(fallback), 4,"Fallback language code should not exceed 4 characters")

