import aiohttp
import asyncio
import re, json
from aiolimiter import AsyncLimiter
import logging

# from charset_normalizer import logging


from pytest_qatouch.utils import (
    QATOUCH_API_END_POINT,
    QatouchRequestError,
    TEST_CASE_STATUS,
)

FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class QatouchAPIs:
    def __init__(self, domain: str, api_token: str, project_key: str):
        self.results = []
        self._domain = domain
        self._api_token = api_token
        self._project_key = project_key
        self._headers = {"domain": self._domain, "api-token": self._api_token}
        self._session = None
        self._limiter = AsyncLimiter(
            max_rate=45, time_period=60
        )  # The Qatouch limit is 50 requests per min (45 to be safer)

    async def __get_session(self):
        self._session = aiohttp.ClientSession()
        return self

    def __enter__(self):
        return asyncio.get_event_loop().run_until_complete(self.__get_session())

    def __exit__(self, *err):
        asyncio.run(self._session.close())
        self._session = None

    async def __fetch_tcs(self, url, page_num, get_lastlink=False):
        async with self._limiter:
            async with self._session.get(
                f"{url}&page={page_num}", headers=self._headers
            ) as response:
                if response.status == 200:
                    res = await response.json()
                    if res.get("data"):
                        tc_keys = []
                        for tc in res.get("data"):
                            tc_keys.append(tc["case_key"])

                        log.debug(
                            f"The qatouch request updated test run successfully {json.dumps(res)}"
                        )
                        if get_lastlink:
                            return tc_keys, res["link"]["last"]
                        else:
                            return tc_keys

                    else:
                        raise QatouchRequestError(
                            f"The qatouch request failed with {[res.get('msg')]}"
                        )

                else:
                    raise QatouchRequestError(
                        f"""Expected to have 200 for the qatoch request but got {response.status},
                                Please make sure the specified domain and API token are right."""
                    )

    async def __fetch_all_tcs(self, url):
        pagination_pages = 1
        tcs_keys, link = await self.__fetch_tcs(url, 1, get_lastlink=True)
        pagination_pages = int(re.search("(?<=page\\=)\\d+", link).group())
        log.debug(f"The number of pages are {pagination_pages}")
        if pagination_pages == 1:
            return tcs_keys
        tasks = [self.__fetch_tcs(url, i) for i in range(2, pagination_pages + 1)]
        groups = await asyncio.gather(*tasks)
        for group in groups:
            tcs_keys = tcs_keys + group
        return tcs_keys

    def get_all_automation_tcs_keys(self):
        url = f"{QATOUCH_API_END_POINT}/getAllTestCases/{self._project_key}/?mode=Automation"
        return asyncio.get_event_loop().run_until_complete(self.__fetch_all_tcs(url))

    def create_testrun(self, assign_to, milestone_key, test_run_name, testcases):
        url = f"{QATOUCH_API_END_POINT}/testRun/specific"
        request_params = {
            "projectKey": self._project_key,
            "assignTo": assign_to,
            "milestoneKey": milestone_key,
            "testRun": test_run_name,
        }

        return asyncio.get_event_loop().run_until_complete(
            self.__create_testrun(url, request_params, {"caseId[]": testcases})
        )

    async def __create_testrun(self, url, request_params, testcases):
        async with self._limiter:
            async with self._session.post(
                url, headers=self._headers, params=request_params, data=testcases
            ) as response:
                if response.status == 200:
                    res = await response.json()
                    if res.get("success"):
                        log.debug(
                            f"The qatouch request updated test run successfully {json.dumps(res)}"
                        )
                        return res.get("data")[0]["testrun_id"]
                    else:
                        raise QatouchRequestError(
                            f"The qatouch request failed with {[res.get('error_msg')]}"
                        )

                else:
                    raise QatouchRequestError(
                        f"""Expected to have 200 for the qatoch request but got {response.status},
                        Please make sure the specified domain and API token are right."""
                    )

    def update_testrun_results(self, results, testrun_key, comments):
        url = f"{QATOUCH_API_END_POINT}/testRunResults/status/multiple"
        request_params = {
            "project": self._project_key,
            "test_run": testrun_key,
            "comments": comments,
            "result": json.dumps(results, separators=(",", ":")),
        }
        asyncio.get_event_loop().run_until_complete(
            self.__update_testrun_results(url, request_params)
        )

    async def __update_testrun_results(self, url, request_params):
        async with self._limiter:
            async with self._session.patch(
                url, headers=self._headers, params=request_params
            ) as response:
                if response.status == 200:
                    res = await response.json()
                    if res.get("success"):
                        log.debug(
                            f"The qatouch request updated test run successfully {json.dumps(res)}"
                        )
                    else:
                        raise QatouchRequestError(
                            f"The qatouch request failed with {[res.get('error_msg')]}"
                        )

                else:
                    raise QatouchRequestError(
                        f"""Expected to have 200 for the qatoch request but got {response.status},
                        Please make sure the specified domain and API token are right."""
                    )


URL = "https://api.qatouch.com/api/v1/getAllTestCases/1gEb/?mode=Automation"  # 3b9e   1gEb
HEADERS = {
    "domain": "xyz",
    "api-token": "dfc",
}

if __name__ == "__main__":
    with QatouchAPIs(
        domain="xyz",
        api_token="dfc",
        project_key="1gEb",
    ) as qatouch_apis:
        RESULTS = [
            {"case": 1, "status": TEST_CASE_STATUS["passed"]},
            {"case": 4, "status": TEST_CASE_STATUS["passed"]},
            {"case": 5, "status": TEST_CASE_STATUS["failed"]},
            {"case": 2, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 3, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 6, "status": TEST_CASE_STATUS["passed"]},
            {"case": 8, "status": TEST_CASE_STATUS["failed"]},
            {"case": 9, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 10, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 13, "status": TEST_CASE_STATUS["passed"]},
            {"case": 14, "status": TEST_CASE_STATUS["passed"]},
            {"case": 16, "status": TEST_CASE_STATUS["failed"]},
            {"case": 28, "status": TEST_CASE_STATUS["passed"]},
            {"case": 56, "status": TEST_CASE_STATUS["passed"]},
            {"case": 7, "status": TEST_CASE_STATUS["passed"]},
            {"case": 17, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 27, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 38, "status": TEST_CASE_STATUS["failed"]},
            {"case": 39, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 41, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 43, "status": TEST_CASE_STATUS["passed"]},
            {"case": 44, "status": TEST_CASE_STATUS["passed"]},
            {"case": 45, "status": TEST_CASE_STATUS["failed"]},
            {"case": 46, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 48, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 58, "status": TEST_CASE_STATUS["passed"]},
            {"case": 61, "status": TEST_CASE_STATUS["passed"]},
            {"case": 62, "status": TEST_CASE_STATUS["failed"]},
            {"case": 63, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 64, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 65, "status": TEST_CASE_STATUS["passed"]},
            {"case": 57, "status": TEST_CASE_STATUS["passed"]},
            {"case": 68, "status": TEST_CASE_STATUS["failed"]},
            {"case": 71, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 72, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 73, "status": TEST_CASE_STATUS["passed"]},
            {"case": 74, "status": TEST_CASE_STATUS["passed"]},
            {"case": 75, "status": TEST_CASE_STATUS["failed"]},
            {"case": 76, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 77, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 78, "status": TEST_CASE_STATUS["passed"]},
            {"case": 79, "status": TEST_CASE_STATUS["passed"]},
            {"case": 80, "status": TEST_CASE_STATUS["failed"]},
            {"case": 87, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 96, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 89, "status": TEST_CASE_STATUS["passed"]},
            {"case": 90, "status": TEST_CASE_STATUS["passed"]},
            {"case": 91, "status": TEST_CASE_STATUS["failed"]},
            {"case": 93, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 92, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 93, "status": TEST_CASE_STATUS["passed"]},
            {"case": 92, "status": TEST_CASE_STATUS["passed"]},
            {"case": 95, "status": TEST_CASE_STATUS["failed"]},
            {"case": 98, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 99, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 100, "status": TEST_CASE_STATUS["passed"]},
            {"case": 101, "status": TEST_CASE_STATUS["passed"]},
            {"case": 967, "status": TEST_CASE_STATUS["failed"]},
            {"case": 104, "status": TEST_CASE_STATUS["skipped"]},
            {"case": 105, "status": TEST_CASE_STATUS["skipped"]},
        ]
        """
        test_cases = qatouch_apis.get_all_automation_tcs_keys()
        print(test_cases)
        testrun = qatouch_apis.create_testrun(
            assign_to="b92R",
            milestone_key="v6GV",
            test_run_name="From python DELETE IT",
            testcases=test_cases,
        )
        """
        print(json.dumps(RESULTS, separators=(",", ":")))
        testrun = "LlQZ"  # "mPml"
        print(
            qatouch_apis.update_testrun_results(
                results=RESULTS,
                testrun_key=testrun,
                comments="Status changed by pytest-qatouch plugin.",
            )
        )

# print(get_qatouch_tcs_key(URL, HEADERS))
