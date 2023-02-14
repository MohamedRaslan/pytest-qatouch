# -*- coding: utf-8 -*-

import pytest
from .utils import QATOUCH_MARK, MissingQatouchData, ExpectedIntegerValue
from .qatouch import QatouchTestResult

__QATOUCH_TEST_RSESULT = None
___Enable_PLUGIN = None


def pytest_addoption(parser):
    group = parser.getgroup("QaTouch")

    def add_option(option, dest, help, default=None, type=None, **kwargs):
        group.addoption(option, dest=dest, default=default, **kwargs)
        parser.addini(dest, default=default, type=type, help=help)

    add_option(
        option="--qatouch",
        action="store",
        dest="qatouch",
        default="Disabled",
        help="Enable the qatouch plugin (Set ['True', 'False'])",
    )

    add_option(
        option="--qatouch-subdomain",
        action="store",
        dest="qatouch-subdomain",
        help="Your qatouch submodule name (i.e <your_subdomain>.qatouch.com)",
    )

    add_option(
        "--qatouch-api-token",
        action="store",
        dest="qatouch-api-token",
        help="Your qatouch API token",
    )

    add_option(
        "--qatouch-project-key",
        action="store",
        dest="qatouch-project-key",
        help="The qatouch project key",
    )

    add_option(
        "--qatouch-testrun-key",
        action="store",
        dest="qatouch-testrun-key",
        help="The testrun key in qatouch project",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", f"{QATOUCH_MARK}(TR): Mark test")
    global ___Enable_PLUGIN
    ___Enable_PLUGIN = (
        str(config.getoption("--qatouch")).lower() == "true"
        or str(config.getini("qatouch")).lower() == "true"
    )

    if( str(config.getoption("--qatouch")).lower() == "false" ):
        ___Enable_PLUGIN= False


    if ___Enable_PLUGIN:

        def get_option(option: str):
            value = config.getoption("--" + option) or config.getini(option)
            if value is None:
                raise MissingQatouchData(
                    f"The option ['--'{option}] or the ini option[{option}] not set"
                )
            return value

        global __QATOUCH_TEST_RSESULT
        __QATOUCH_TEST_RSESULT = QatouchTestResult(
            domain=get_option("qatouch-subdomain"),
            api_token=get_option("qatouch-api-token"),
            project_key=get_option("qatouch-project-key"),
            testrun_key=get_option("qatouch-testrun-key"),
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    test_result = outcome.get_result()
    qa_marker = item.get_closest_marker(QATOUCH_MARK)
    if __QATOUCH_TEST_RSESULT and qa_marker:
        if test_result.when == "call":
            __add_test(qa_marker, test_result)

        elif test_result.when in ("setup", "teardown") and test_result.outcome != "passed":
            __add_test(qa_marker, test_result)


def pytest_sessionfinish():
    global __QATOUCH_TEST_RSESULT
    if ___Enable_PLUGIN and __QATOUCH_TEST_RSESULT:
        __QATOUCH_TEST_RSESULT.push_results_to_qatouch()
        __QATOUCH_TEST_RSESULT = None


def __add_test(qa_marker, test_result):
    if "TR" in qa_marker.kwargs:
        tr_value = qa_marker.kwargs["TR"]
        if not isinstance(tr_value, int):
            raise ExpectedIntegerValue(
                f"Expected the TR value to be a valid integer value bug insted got {tr_value} of type {type(tr_value)}"
            )
    else:
        raise MissingQatouchData(f"Expected to have a TR and its value, but not found")

    __QATOUCH_TEST_RSESULT.push_testcase_to_results(
        testcase_id=tr_value, testcase_status=test_result.outcome
    )
