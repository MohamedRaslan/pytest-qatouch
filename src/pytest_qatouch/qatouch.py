import requests
import json
import pytest

from .utils import (
    TEST_CASE_STATUS,
    QATOUCH_API_END_POINT,
    WrongQatouchStatus,
    QatouchRequestError,
)


def TR(value: int):
    return pytest.mark.qatouch(TR=value)


class QatouchTestResult:
    def __init__(self, domain: str, api_token: str, project_key: str, testrun_key: str):
        self.results = []
        self.domain = domain
        self.api_token = api_token
        self.project_key = project_key
        self.testrun_key = testrun_key

    def push_testcase_to_results(self, testcase_id: int, testcase_status: str) -> None:
        if testcase_status.lower() in TEST_CASE_STATUS:
            status = TEST_CASE_STATUS.get(testcase_status.lower())
            self.results.append({"case": testcase_id, "status": status})
        else:
            raise WrongQatouchStatus(
                f"Expected to have one of the following status ['passed','skipped','failed'] but we got [{testcase_status}]"
            )

    def push_results_to_qatouch(self) -> str:
        request_url = QATOUCH_API_END_POINT + "/testRunResults/status/multiple"
        request_headers = {"domain": self.domain, "api-token": self.api_token}
        request_payload = {
            "project": self.project_key,
            "test_run": self.testrun_key,
            "comments": "Status changed by pytest-qatouch plugin.",
            "result": json.dumps(self.results),
        }

        response = requests.patch(
            request_url, headers=request_headers, params=request_payload
        )

        if response.status_code == 200:
            if response.json().get("success"):
                print(
                    f"\nThe qatouch request updated the test run successfully with response : \n{json.dumps(response.json())}"
                )
            else:
                raise QatouchRequestError(
                    f"The qatouch request failed because {[response.json().get('error_msg')]}"
                )

        else:
            raise QatouchRequestError(
                f"""Expected to have 200 for the qatoch request but got {response.status_code},
                    Please make sure the specified domain and API token are right."""
            )
