import os
import pytest
import tempfile
import updatemyip
import updatemyip.meta as meta
import updatemyip.provider as provider


test_providers_path = os.path.join(os.path.dirname(__file__), "providers")
provider.import_modules(test_providers_path)


@pytest.fixture
def test_state_path():
    return os.path.join(
        tempfile.gettempdir(),
        f"{meta.NAME}.test_state"
    )


@pytest.fixture
def test_state(test_state_path):
    updatemyip.state_write("", path=test_state_path)
    return test_state_path
