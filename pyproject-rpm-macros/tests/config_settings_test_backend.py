"""
This is a test backend for pyproject-rpm-macros' integration tests
It is not compliant with PEP 517 and omits some required hooks.
"""

from flit_core import buildapi
from packaging.version import parse
from pip import __version__ as pip_version

EXPECTED_CONFIG_SETTINGS = [{"abc": "123", "xyz": "456", "--option-with-dashes": ["1", "2"]}]
# Older pip did not accept multiple values,
# but we might backport that later,
# hence we accept it both ways with older pips
if parse(pip_version) < parse("23.1"):
    EXPECTED_CONFIG_SETTINGS.append(
        EXPECTED_CONFIG_SETTINGS[0] | {"--option-with-dashes": "2"}
    )


def _verify_config_settings(config_settings):
    print(f"config_settings={config_settings}")
    if config_settings not in EXPECTED_CONFIG_SETTINGS:
        raise ValueError(
            f"{config_settings!r} does not match expected {EXPECTED_CONFIG_SETTINGS!r}"
        )


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _verify_config_settings(config_settings)
    return buildapi.build_wheel(wheel_directory, None, metadata_directory)


def get_requires_for_build_wheel(config_settings=None):
    _verify_config_settings(config_settings)
    return buildapi.get_requires_for_build_wheel(None)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    _verify_config_settings(config_settings)
    return buildapi.prepare_metadata_for_build_wheel(metadata_directory, None)
