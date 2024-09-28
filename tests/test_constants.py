import os
import unittest
from unittest.mock import patch

from betterenvs import ConfigureVariables, VariableSpecification


class TestConstantVariables(unittest.TestCase):
    def test_configure_variables(self):
        class Variables:
            VAR1 = VariableSpecification(
                datatype=str, required=False, default_value="default1"
            )
            VAR2 = VariableSpecification(datatype=int, required=True)
            VAR3 = "constant"

        with patch.dict(os.environ, {"VAR2": "2"}, clear=True):
            ConfigureVariables(Variables)

        self.assertEqual(Variables.VAR1, "default1")
        self.assertEqual(Variables.VAR2, 2)
        self.assertEqual(Variables.VAR3, "constant")
