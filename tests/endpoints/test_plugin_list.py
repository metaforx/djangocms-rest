from django.urls import reverse

from tests.base import BaseCMSRestTestCase
from tests.utils import assert_field_types


class PluginListTestCase(BaseCMSRestTestCase):
    def test_get(self):

        type_checks = {
            "plugin_type": str,
            "title": str,
            "type": str,
            "properties": dict,
        }

        # GET
        response = self.client.get(reverse("plugin-list"))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Data & Type Validation
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0, "Plugin list should not be empty")

        # Check Plugin Types
        for plugin in data:
            for field, expected_type in type_checks.items():
                assert_field_types(
                    self,
                    plugin,
                    field,
                    expected_type,
                    f"plugin {plugin.get('plugin_type', 'unknown')}",
                )
