import os
import unittest

from betterenvs import ConfigureVariables, VariableSpecification


class BetterenvsTest(unittest.TestCase):
    def test_non_required_without_default_value(self):
        class Variables:
            NON_REQUIRED_VARIABLE = VariableSpecification(
                datatype=int, required=False, default_value=None
            )

        ConfigureVariables(Variables)
        self.assertIsNone(Variables.NON_REQUIRED_VARIABLE)

    def test_non_required_with_default_value_expected_datatype(self):
        default_value = 100
        required_datatype = int

        class Variables:
            NON_REQUIRED_VARIABLE = VariableSpecification(
                datatype=required_datatype, required=False, default_value=default_value
            )

        ConfigureVariables(Variables)
        self.assertEqual(type(Variables.NON_REQUIRED_VARIABLE),
                         required_datatype)

    def test_non_required_with_default_value_unexpected_datatype(self):
        default_value = "100"
        required_datatype = int

        class Variables:
            NON_REQUIRED_VARIABLE = VariableSpecification(
                datatype=required_datatype, required=False, default_value=default_value
            )

        ConfigureVariables(Variables)
        self.assertEqual(type(Variables.NON_REQUIRED_VARIABLE),
                         required_datatype)

    def test_required_without_value(self):
        class Variables:
            REQUIRED_VARIABLE = VariableSpecification(
                datatype=int, required=True, default_value=None
            )

        with self.assertRaises(Exception) as context:
            ConfigureVariables(Variables)
            self.assertTrue(
                "Variable REQUIRED_VARIABLE is required and not found in the Environment..."
                in context.exception
            )

    def test_required_with_value(self):
        default_value = None
        required_datatype = int
        os.environ["REQUIRED_VARIABLE"] = "10"

        class Variables:
            REQUIRED_VARIABLE = VariableSpecification(
                datatype=required_datatype, required=False, default_value=default_value
            )

        ConfigureVariables(Variables)
        self.assertEqual(type(Variables.REQUIRED_VARIABLE), required_datatype)
        del os.environ["REQUIRED_VARIABLE"]

    def test_required_with_value_custom_name(self):
        default_value = None
        required_datatype = int
        os.environ["REQUIRED_VARIABLE_CUSTOM_NAME"] = "10"

        class Variables:
            REQUIRED_VARIABLE = VariableSpecification(
                datatype=required_datatype,
                required=False,
                default_value=default_value,
                custom_name="REQUIRED_VARIABLE_CUSTOM_NAME",
            )

        ConfigureVariables(Variables)
        self.assertEqual(type(Variables.REQUIRED_VARIABLE), required_datatype)
        del os.environ["REQUIRED_VARIABLE_CUSTOM_NAME"]
