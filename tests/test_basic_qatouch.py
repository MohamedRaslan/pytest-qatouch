import re
import json
import responses

from pytest_qatouch.utils import TEST_CASE_STATUS, QATOUCH_API_END_POINT


TESTS = """
        import pytest
        from pytest_qatouch import qatouch

        @qatouch.TR(1)
        def test_one():
            assert True

        @qatouch.TR(2)
        def test_two():
            assert True

        @qatouch.TR(3)
        def test_three():
            assert False

        @qatouch.TR(4)
        @pytest.mark.skip
        def test_four():
            assert True

        @qatouch.TR(5)
        @pytest.mark.skip
        def test_five():
            assert False
        """

SUBDOMAIN = "example"
API_TOKEN = "example1645df54fgdf6g5446dg654"
PROJECT_KEY = "L6df"
TESTRUN_KEY = "M5Rd"
RESULTS = [
    {"case": 1, "status": TEST_CASE_STATUS["passed"]},
    {"case": 2, "status": TEST_CASE_STATUS["passed"]},
    {"case": 3, "status": TEST_CASE_STATUS["failed"]},
    {"case": 4, "status": TEST_CASE_STATUS["skipped"]},
    {"case": 5, "status": TEST_CASE_STATUS["skipped"]},
]

REQUEST_URL = QATOUCH_API_END_POINT + "/testRunResults/status/multiple"
REQUEST_HEADERS = {"domain": SUBDOMAIN, "api-token": API_TOKEN}
REQUEST_PAYLOAD = {
    "project": PROJECT_KEY,
    "test_run": TESTRUN_KEY,
    "comments": "Status changed by pytest-qatouch plugin.",
    "result": json.dumps(RESULTS),
}

RESPONSE_BODY = json.dumps({"success": True, "msg": f"updated test run's status to {TESTRUN_KEY}"})
STDOUT_MSG = f"The qatouch request updated the test run successfully with response : \n{RESPONSE_BODY}"


def test_using_all_options(testdir, mock):
    mock.add(
        responses.Response(
            method="PATCH",
            url=REQUEST_URL,
            headers=REQUEST_HEADERS,
            body=RESPONSE_BODY,
            status=200,
            content_type="application/json",
        )
    )
    testdir.makepyfile(TESTS)
    result = testdir.runpytest(
        "--qatouch=True",
        f"--qatouch-subdomain={SUBDOMAIN}",
        f"--qatouch-api-token={API_TOKEN}",
        f"--qatouch-project-key={PROJECT_KEY}",
        f"--qatouch-testrun-key={TESTRUN_KEY}",
    )
    assert result.ret == 1
    result.assert_outcomes(passed=2, skipped=2, failed=1)
    stdout = result.stdout.str()
    assert re.search(STDOUT_MSG, stdout)


def test_using_all_inioptions(testdir, mock):
    mock.add(
        responses.Response(
            method="PATCH",
            url=REQUEST_URL,
            headers=REQUEST_HEADERS,
            body=RESPONSE_BODY,
            status=200,
            content_type="application/json",
        )
    )
    testdir.makepyfile(TESTS)
    testdir.makeini(
        f"""
        [pytest]
        qatouch             = True
        qatouch-subdomain   = {SUBDOMAIN}
        qatouch-api-token   = {API_TOKEN}
        qatouch-project-key = {PROJECT_KEY}
        qatouch-testrun-key = {TESTRUN_KEY}
        """
    )
    result = testdir.runpytest()
    assert result.ret == 1
    result.assert_outcomes(passed=2, skipped=2, failed=1)
    stdout = result.stdout.str()
    assert re.search(STDOUT_MSG, stdout)
