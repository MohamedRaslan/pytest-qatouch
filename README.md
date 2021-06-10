# pytest-qatouch

Pytest plugin for uploading test results to your QA Touch Testrun.

## Features

- It only will upload the test results to the specified testrun in your Qatouch portal

pytest-plugin testrail pytest-pytestrail

## Installation

You can install "pytest-qatouch" via **[pip](https://pypi.org/project/pip/)** from **[PyPI](https://pypi.org/project/pytest-qatouch/)**::

```shell
pip install pytest-pytestrail
```

## Usage

```python
from pytest_qatouch import qatouch


@qatouch.TR(10)
def test_for_testcase_number0010():
    assert True

@qatouch.TR(9)
def test_for_testcase_number0009():
    assert False
```

And If you want to use it with a parameterized tests , you can do as the example below.

```python
import pytest
from pytest_qatouch import qatouch

@pytest.mark.parametrize(
    "num1,num2",
    [
        (9, 8),
        pytest.param(8, 10, marks=qatouch.TR(2)),
        pytest.param(0, 10, marks=qatouch.TR(10)),
        pytest.param(1, 4, marks=qatouch.TR(9)),
    ],
)
def test_six(num1, num2):
    assert num1+num2 >= 10
```

### Configuration

You can use a **config file** or pass it to `pytest` as **command line options**.

#### Config file

`pytest.ini` or `setup.cfg` **[pytest configuration](https://docs.pytest.org/en/latest/customize.html)**

```ini
[pytest]
qatouch (string):                        Enable the qatouch plugin (Set it to 'True' to enable it)
qatouch-subdomain (string):              Your qatouch submodule name (i.e <your_subdomain>.qatouch.com)
qatouch-api-token (string):              Your qatouch API token
qatouch-project-key (string):            The qatouch project key
qatouch-testrun-key (string):            The testrun key in qatouch project
```

#### Command line options

```bash
--qatouch                        Enable the qatouch plugin (Set it to 'True' to enable it)
--qatouch-subdomain              Your qatouch submodule name (i.e <your_subdomain>.qatouch.com)
--qatouch-api-token              Your qatouch API token
--qatouch-project-key            The qatouch project key
--qatouch-testrun-key            The testrun key in qatouch project
```

## Issues

If you encounter any problems, please **[file an issue](https://github.com/MohamedRaslan/pytest-qatouch/issues)** along with a detailed description.

## Contributing

Contributions are very welcome.
