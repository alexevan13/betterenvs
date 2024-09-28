import os
import uuid
from typing import Any, Optional, final

import yaml


@final
class VariableSpecification:
    def __init__(
        self,
        datatype: Any,
        required: bool,
        default_value: Optional[Any] = None,
        custom_name: Optional[str] = None,
    ):
        self.datatype = datatype
        self.required = required
        self.default_value = default_value
        self.custom_name = custom_name


@final
class ConfigureVariables:
    def __new__(cls, variables_cls):
        def get(name, spec_obj):
            if spec_obj.custom_name:
                name = spec_obj.custom_name
            value = os.environ.get(name, spec_obj.default_value)
            if not value:
                if spec_obj.required:
                    raise AttributeError(
                        f"Variable {name} is required and not found in the Environment..."
                    )
                return None
            if spec_obj.datatype == bool:
                return eval(value.capitalize())
            return spec_obj.datatype(value)

        for var, val in vars(variables_cls).items():
            if not (var.startswith("_") or callable(val)):
                if isinstance(val, VariableSpecification):
                    setattr(variables_cls, var, get(var, val))
                else:
                    setattr(variables_cls, var, val)


@final
class Settings:
    _instance = None

    def __new__(cls, settings_yaml_file="settings.yaml"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings_yaml_file = settings_yaml_file
            cls._instance.loaded_settings = None
        return cls._instance

    @staticmethod
    def __set_env_variables(config, into):
        for key, value in config.get("env-variables", {}).items():
            att_name = value.get("custom-name") or key.replace("-", "_").upper()
            into[att_name] = VariableSpecification(
                datatype=eval(value.get("datatype", "str")),
                required=value.get("required", True),
                default_value=value.get("default"),
                custom_name=value.get("custom-name"),
            )

    @staticmethod
    def __set_constants(config, into):
        for key, value in config.get("constants", {}).items():
            att_name = key.replace("-", "_").upper()
            into[att_name] = (
                str(value["value"])
                if not value.get("datatype")
                else eval(value["datatype"])(value["value"])
            )

    @classmethod
    def load_settings(cls, settings_yaml_file):
        if cls._instance is None:
            cls._instance = cls(settings_yaml_file)
        if cls._instance.loaded_settings is None:
            with open(cls._instance.settings_yaml_file) as f:
                config = yaml.safe_load(f)
                attributes = {}
                cls.__set_env_variables(config, into=attributes)
                cls.__set_constants(config, into=attributes)
            class_name = uuid.uuid4().hex
            settings = type(class_name, (), attributes)
            ConfigureVariables(settings)
            cls._instance.loaded_settings = settings

    @classmethod
    def get_settings(cls):
        if cls._instance is None or cls._instance.loaded_settings is None:
            raise RuntimeError(
                "Settings not loaded. Use Settings.load_settings() before calling get_settings()."
            )
        return cls._instance.loaded_settings
