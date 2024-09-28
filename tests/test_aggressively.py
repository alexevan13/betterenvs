import os
import unittest
from unittest.mock import patch

from betterenvs import ConfigureVariables, VariableSpecification


class TestConfigureVariables(unittest.TestCase):
    def setUp(self):
        # Set up environment variables for testing
        os.environ["TEST_VAR_1"] = "42"
        os.environ["TEST_VAR_2"] = "Hello World"
        os.environ["TEST_VAR_3"] = ""
        os.environ["TEST_VAR_4"] = "3.14"
        os.environ["TEST_VAR_5"] = "True"
        os.environ["TEST_VAR_6"] = "False"

    def test_configure_variables_with_custom_names(self):
        # Create a model class
        class Variables:
            TEST_VAR_1 = VariableSpecification(
                int, True, custom_name="CUSTOM_VAR_NAME_1"
            )
            TEST_VAR_2 = VariableSpecification(
                str, True, custom_name="CUSTOM_VAR_NAME_2"
            )

        # Configure variables with custom names
        with patch.dict(
            os.environ, {"CUSTOM_VAR_NAME_1": "42",
                         "CUSTOM_VAR_NAME_2": "Hello World"}
        ):
            ConfigureVariables(Variables)

        # Check variables were configured correctly
        self.assertEqual(Variables.TEST_VAR_1, 42)
        self.assertEqual(Variables.TEST_VAR_2, "Hello World")

    def test_configure_variables_with_partial_configuration(self):
        # Create a model class
        class Variables:
            TEST_VAR_1 = VariableSpecification(int, True)
            TEST_VAR_2 = VariableSpecification(str, True)
            TEST_VAR_3 = VariableSpecification(bool, True)
            TEST_VAR_4 = VariableSpecification(bool, False)

        # Configure variables with only required variables set
        with patch.dict(os.environ, {"TEST_VAR_1": "42", "TEST_VAR_2": "Hello World", "TEST_VAR_3": "False"}):
            ConfigureVariables(Variables)

        # Check variables were configured correctly
        self.assertEqual(Variables.TEST_VAR_1, 42)
        self.assertEqual(Variables.TEST_VAR_2, "Hello World")
        self.assertEqual(Variables.TEST_VAR_3, False)

    def test_configure_variables_with_extra_configuration(self):
        # Create a model class with extra variables not set in environment
        class Variables:
            TEST_VAR_1 = VariableSpecification(int, True)
            TEST_VAR_2 = VariableSpecification(str, True)
            # Configure variables with only required variables set

        with patch.dict(os.environ, {"TEST_VAR_1": "42", "TEST_VAR_2": "Hello World"}):
            ConfigureVariables(Variables)

        # Check variables were configured correctly
        self.assertEqual(Variables.TEST_VAR_1, 42)
        self.assertEqual(Variables.TEST_VAR_2, "Hello World")

    def test_configure_variables_with_no_configuration(self):
        # Create a model class with no variables
        class Variables:
            pass

        # Configure variables with no variables
        ConfigureVariables(Variables)

        # Check that no variables were set
        self.assertFalse(hasattr(Variables, "TEST_VAR_1"))
        self.assertFalse(hasattr(Variables, "TEST_VAR_2"))
