import pytest
import responses

pytest_plugins = ["pytester"]


@pytest.fixture
def mock():
    with responses.RequestsMock() as rsps:
        yield rsps
