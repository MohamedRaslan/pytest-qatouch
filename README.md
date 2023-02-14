![Qatouch integration with pytest](https://github.com/MohamedRaslan/pytest-qatouch/blob/main/doc/images/pytest-qatouch.png?raw=true 'Qatouch integration with pytest')
___
[![PyPI](https://img.shields.io/pypi/v/pytest-qatouch?color=blue&label=version&logo=python&logoColor=blue)](https://pypi.org/project/pytest-qatouch/) [![Downloads](https://static.pepy.tech/personalized-badge/pytest-qatouch?period=total&units=international_system&left_color=grey&right_color=blue&left_text=downloads)](https://pepy.tech/project/pytest-qatouch)[![Python package](https://github.com/MohamedRaslan/pytest-qatouch/actions/workflows/code-test.yml/badge.svg)](https://github.com/MohamedRaslan/pytest-qatouch/actions/workflows/code-test.yml) [![codecov](https://codecov.io/gh/MohamedRaslan/pytest-qatouch/branch/main/graph/badge.svg?token=SD4WWNE48S)](https://codecov.io/gh/MohamedRaslan/pytest-qatouch)

[![GitHub stars](https://img.shields.io/github/stars/MohamedRaslan/pytest-qatouch)](https://github.com/MohamedRaslan/pytest-qatouch/stargazers) [![GitHub forks](https://img.shields.io/github/forks/MohamedRaslan/pytest-qatouch)](https://github.com/MohamedRaslan/pytest-qatouch/network) [![GitHub issues](https://img.shields.io/github/issues/MohamedRaslan/pytest-qatouch)](https://github.com/MohamedRaslan/pytest-qatouch/issues) [![GitHub Release Date](https://img.shields.io/github/release-date/mohamedraslan/pytest-qatouch)](https://github.com/MohamedRaslan/pytest-qatouch/releases) [![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mohamedraslan/pytest-qatouch)](https://github.com/MohamedRaslan/pytest-qatouch)

# pytest-qatouch

Pytest plugin for uploading test results to your QA Touch Testrun.

## Features

- It only will upload the test results to the specified testrun in your Qatouch portal


## Installation

You can install "pytest-qatouch" via **[pip](https://pypi.org/project/pip/)** from **[PyPI](https://pypi.org/project/pytest-qatouch/)**::

```shell
pip install pytest-qatouch
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
def test_sum_greater_than10(num1, num2):
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

## User guide
For further documentation see **[wiki](https://github.com/MohamedRaslan/pytest-qatouch/wiki)** and checkout this video:
[![Qatouch integration with pytest](https://github.com/MohamedRaslan/pytest-qatouch/blob/main/doc/images/Thumbnail.png?raw=true)](https://www.youtube.com/watch?v=tC_qbNr_M0k 'Qatouch integration with pytest')


## Issues

If you encounter any problems, please **[file an issue](https://github.com/MohamedRaslan/pytest-qatouch/issues)** along with a detailed description.

## Contributing

Contributions are very welcome.

## Development

To start development,run your python environment then run the following commands:

```shell
# Update pip, wheel and setuptools
python -m pip install -U pip wheel setuptools

# Instal all the needed dependencies
pip install -e .[dev]
```
