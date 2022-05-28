import os
import tempfile

import pytest

import mcddns
import mcddns.provider as provider


test_providers_path = os.path.join(os.path.dirname(__file__), "provider")
provider.import_modules(test_providers_path)


@pytest.fixture
def test_state_path():
    return os.path.join(tempfile.gettempdir(), f"{mcddns.META['Name']}.test_state")


@pytest.fixture
def test_state(test_state_path):
    mcddns.state_write("", path=test_state_path)
    return test_state_path
