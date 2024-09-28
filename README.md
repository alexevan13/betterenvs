## BetterEnvs
#### A better way to manage environment variables and settings

- `betterenvs` is a Python library designed to handle environment variables and settings in a structured manner. It offers classes and decorators for defining environment variables' requirements and their associated data types.

### Installation

You can install `betterenvs` using pip:

```bash
pip install .
```

### Usage

1. **Defining Environment Variables**

   - Import the necessary classes from `betterenvs`:

     ```python
     from betterenvs import ConfigureVariables, VariableSpecification
     ```

   - Create a class to define your environment variables and their specifications:

     ```python
     class Variables:
         LOG_LEVEL = VariableSpecification(
             datatype=str, required=True, default_value="DEBUG", custom_name=None
         )
         AWS_REGION = VariableSpecification(
             datatype=str, required=True, default_value=None, custom_name=None
         )
     ```

   - Use `ConfigureVariables` to set up the environment variables:

     ```python
     ConfigureVariables(Variables)
     ```

   #### Alternatively, you can use the `Settings` class to load settings from a YAML file:
    - settings.yaml
    ```yaml
    env-variables:
      log-level:
        default: DEBUG
        required: true
      aws-region:
        required: true

    constants:
      service-name:
        datatype: str
        value: test-example
      test-const:
        value: 100
        datatype: int

    ```

    - app.py
     ```python
     import os
     from betterenvs import Settings

     Settings.load_settings(os.path.join(os.path.dirname(__file__), "settings.yaml"))
     ```

2. **Accessing Environment Variables and Constants**

   - After configuration or loading settings, you can access environment variables and constants as attributes of the appropriate class or settings object:

     ```python
     # Using ConfigureVariables approach
     print(Variables.LOG_LEVEL)
     print(Variables.AWS_REGION)

     settings = Settings.get_settings()
     # Using Settings approach
     print(settings.LOG_LEVEL)
     print(settings.AWS_REGION)
     print(settings.SERVICE_NAME)
     print(settings.TEST_CONST)
     ```

### Quickstart Example Using `Class` approach



```python
# Using ConfigureVariables approach
from betterenvs import ConfigureVariables, VariableSpecification

class Variables:
    LOG_LEVEL = VariableSpecification(
        datatype=str, required=True, default_value="DEBUG", custom_name=None
    )
    AWS_REGION = VariableSpecification(
        datatype=str, required=True, default_value=None, custom_name=None
    )

ConfigureVariables(Variables)

print(Variables.LOG_LEVEL)
print(Variables.AWS_REGION)
```
### Using settings approach
#### Important notes:

- This `Settings.load_settings()` use singleton approach where you load once and you can call `Settings.get_settings()` from anywhere.
- Just load once in the main entrypoint and after that just import Settings and call `Settings.get_settings()` all the settings would be available without reading the yaml file multiple times.

### Quickstart Example Using `Settings` Approach

- settings.yaml
```yaml
env-variables:
  log-level:
    default: DEBUG
    required: true
  aws-region:
    required: true
  other-var:
    default: other_value
    required: true
    custom-name: TEST_VAR

constants:
  service-name:
    datatype: str
    value: test-example
  test-const:
    value: 100
    datatype: int

```
- app.py
```python
# Using Settings approach
from betterenvs import Settings
import os

Settings.load_settings(os.path.join(os.path.dirname(__file__), "settings.yaml"))

settings = Settings.get_settings()

print(settings.LOG_LEVEL)
print(settings.AWS_REGION)
print(settings.SERVICE_NAME)
print(settings.TEST_CONST)
print(settings.TEST_VAR)
```

### License

This project is licensed under the GNU License.
