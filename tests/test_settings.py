import os.path
import unittest

from betterenvs import Settings


class TestSettings(unittest.TestCase):
    def setUp(self) -> None:
        self.settings_file = os.path.join(
            os.path.dirname(__file__), "settings.yaml")

    def test_load_settings(self):
        Settings.load_settings(
            settings_yaml_file=self.settings_file
        )  # Call load_settings directly
        self.assertIsNotNone(Settings._instance.loaded_settings)

    def test_get_settings(self):
        Settings.load_settings(
            settings_yaml_file=self.settings_file
        )  # Load settings first
        loaded_settings = (
            Settings.get_settings()
        )  # Call get_settings directly after loading

        self.assertIsNotNone(loaded_settings)

    def test_load_settings_twice(self):

        Settings.load_settings(settings_yaml_file=self.settings_file)
        Settings.load_settings(
            settings_yaml_file=self.settings_file
        )  # Load settings twice

        self.assertIsNotNone(Settings._instance.loaded_settings)

    def test_get_settings_without_loading(self):
        with self.assertRaises(RuntimeError):
            Settings.get_settings()  # Call get_settings directly

    def test_get_settings_without_instance(self):
        Settings._instance = None  # Simulate no instance created

        with self.assertRaises(RuntimeError):
            Settings.get_settings()  # Call get_settings directly

    def test_settings_attribute_types(self):
        Settings.load_settings(
            settings_yaml_file=self.settings_file
        )  # Load settings first
        settings = Settings.get_settings()
        self.assertEqual(type(settings.LOG_LEVEL), str)
        self.assertEqual(type(settings.AWS_REGION), str)
        self.assertEqual(type(settings.TEST_BOOL), bool)
        self.assertEqual(type(settings.SERVICE_NAME), str)
        self.assertEqual(type(settings.TEST_CONST), int)
        self.assertEqual(type(settings.BOOL_CONST), bool)
