from typing import Literal
from pydantic import BaseModel, Field
from rich import print, pretty
from requests import Response
from uplink import Body, Consumer, Path, Query, get, patch, post
from pytest_qatouch.utils import QATOUCH_API_END_POINT

import json

pretty.install()


class ModeType(BaseModel):
    mode: Literal["Automation", "Manual"]


class QATouch(Consumer):
    def __init__(self, domain, api_token, base_url=QATOUCH_API_END_POINT):
        super(QATouch, self).__init__(base_url=base_url)
        # Send the domain , api_token as default headers with each request.
        self.session.headers["domain"] = domain
        self.session.headers["api-token"] = api_token
        self.session.headers["User-Agent"] = "PyQAtouch client"

    #############
    ## Project ##
    #############

    # List All Projects
    @get("getAllProjects")
    def get_all_projects(self, page: Query = None) -> Response:
        """List all your QA Touch projects ."""

    # Project - Test Case / Milestone / Defect Counts
    @get("getAllProjects/{projectKey}")
    def get_project_summary(self, project_key: Path("projectKey"), page: Query = None) -> Response:
        """Provides the particular project detail with Test Case / Milestone / Defect Counts."""

    # Count Projects
    @get("count/allProjects")
    def get_projects_count(self, page: Query() = None) -> Response:
        """Count of the total projects available."""

    # Create Project
    @post("project")
    def create_new_project(self, name: Query()) -> Response:
        """Create a new project in your domain."""

    ################
    ## Test Cases ##
    ################

    # List Test Cases
    # List Test Cases - Pagination
    @get("getAllTestCases/{projectKey}")
    def get_test_cases_list(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
        module_key: Query("moduleKey") = None,
        mode: Query() = None,
        view: Query() = None,
        requirement_key: Query("requirementKey") = None,
    ) -> Response:
        """Provides the list of test cases available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.
            - module_key (Query, optional): To list all test cases for a particular module.
            - mode (Query, optional): To list all test cases based on the provided mode which is one of ["Automation" , "Manual"].
            - view (Query, optional): To display the count/list of test cases based on the value which
                can either be ["Count" , "List"] count (will give the count of test cases) or list (will give the list of test cases).
            - requirement_key (Query, optional): To list all test cases which are present under the provided requirements.

        Note:
            The above parameters [module_key,mode,view,requirement_key] can be used only one at a time and can't be requested with multiple parameters.
            The view parameter can only be used with mode parameter.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Count Test Cases
    @get("count/allTestCases/{projectKey}")
    def get_test_cases_count(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Count of the total test cases available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Test Cases - Custom Fields
    @get("getTestCasesDetail/{projectKey}/{caseID}")
    def get_test_case_detail(
        self,
        project_key: Path("projectKey"),
        case_id: Path("caseID"),
        page: Query = None,
    ) -> Response:
        """Test Case detail with mapped custom fields information.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - case_id (Path): Your test case id
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Test Cases - Steps Template
    @get("getTestCasesSteps/{caseID}")
    def get_test_case_steps(
        self,
        case_id: Path("caseID"),
        page: Query = None,
    ) -> Response:
        """Test Case detail with Steps detail.

        Args:
            - case_id (Path): Your test case id
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # List all Modules
    @get("getAllModules/{projectKey}")
    def get_test_modules_list(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Provides the list of Modules available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.


        Returns:
            Response: returns the result of type requests.Response
        """

    # Create Module
    @post("module")
    def create_module(
        self,
        project_key: Query("projectKey"),
        module_name: Query("moduleName"),
        parent_module_key: Query("parentKey") = None,
        page: Query = None,
    ) -> Response:
        """Create a new module in your project for Test Case.

        Args:
            - project_key (Query): Your ID / Project Key / Value under which the Module to be created
            - module_name (Query): Name of the module to be created
            - parent_module_key (Query, optional): To create child module, provide this parameter with existing Module's Key
            - page (Query, optional): Pagination page number.
        Returns:
            Response: returns the result of type requests.Response
        """

    # Create Test Cases
    @post("testCase")
    def create_test_case(
        self,
        project_key: Query("projectKey"),
        module_key: Query("sectionKey"),
        title: Query("caseTitle"),
        page: Query = None,
    ) -> Response:
        """Create a new Test Cases in your project.

        Args:
            - project_key (Query): Your ID / Project Key / Value under which the Module to be created
            - module_key (Query): Provide the section/module key for under which the test case should be created
            - title (Query): Title of the test case
            - page (Query, optional): Pagination page number

        Returns:
            Response: returns the result of type requests.Response
        """

    ##############
    ## Releases ##
    ##############

    # List Releases
    @get("getAllMilestones/{projectKey}")
    def get_releases_list(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Provides the list of Releases available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Count Releases
    @get("count/allMilestones/{projectKey}")
    def get_releases_count(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Count of the total Releases available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Create Release
    @post("milestone")
    def create_release(
        self,
        project_key: Query("projectKey"),
        title: Query("milestone"),
        page: Query = None,
    ) -> Response:
        """Create a new Release in your project.

        Args:
            - project_key (Query): Your ID / Project Key / Value under which the Module to be created
            - title (Query): Name of the release to be created
            - page (Query, optional): Pagination page number

        Returns:
            Response: returns the result of type requests.Response
        """

    ################
    ## Test Plans ##
    ################

    # List Test Plans
    @get("getAllTestPlan/{projectKey}")  # Todo (Testing)
    def get_test_plans_list(
        self,
        project_key: Path("projectKey"),
        plans_name: Query("name"),
        page: Query = None,
    ) -> Response:
        """List of Test plans available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - plans_name (Query, optional):To get test plan based on the name provided
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Count Test Plans
    @get("countTestPlan/{projectKey}")
    def get_test_plans_count(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Count of the total Test Plans available for the project.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    ###############
    ## Test Runs ##
    ###############

    # List Test Runs
    # List Test Runs with filters

    @get("getAllTestRuns/{projectKey}")
    def get_test_runs_list(
        self,
        project_key: Path("projectKey"),
        test_runs_name: Query("name"),
        page: Query = None,
    ) -> Response:
        """Provides the list of Test Runs available for the project.
            OR
            Provides the list of Test Runs for the project by filtering the name of Test Runs.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - test_runs_name (Query, optional): To get test run based on the provided name.
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Count Test Runs
    @get("count/allTestRuns/{projectKey}")
    def get_test_runs_count(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Count of the total Test Runs available for the project.


        Args:
            - project_key (Path): Your ID / Project Key / Value
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # List Test Runs detail
    @get("getTestRundetails/{projectKey}/{testrunkey}")
    def get_test_run_detail(
        self,
        project_key: Path("projectKey"),
        test_run_key: Path("testrunkey"),
        page: Query = None,
    ) -> Response:
        """Test Run detail

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - test_run_key (Path): Your test run id/key
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # List Test Run Results
    @get("testRunResults/{projectKey}/{testrunkey}")
    def get_test_run_result(
        self,
        project_key: Path("projectKey"),
        test_run_key: Path("testrunkey"),
        page: Query = None,
    ) -> Response:
        """Provides the list of Test Runs Results available for a Test Run.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - test_run_key (Path): Your test run id/key
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Test Runs & Results mapped with the Test case API
    @get("getTestRunlist/{caseID}")
    def get_test_run_results_for_case(
        self,
        case_id: Path("caseID"),
        page: Query = None,
    ) -> Response:
        """Provides the list of Test Runs Results mapped with a test case.

        Args:
            - case_id (Path): Your test case id
            - page (Query, optional): Pagination page number.
        Returns:
            Response: returns the result of type requests.Response
        """

    # List Test Run Results for Release
    @get("testRunResults/{projectKey}/{releaseKey}")
    def get_test_run_results_for_release(
        self,
        project_key: Path("projectKey"),
        release_key: Path("releaseKey"),
        status: Query = None,
        page: Query = None,
    ) -> Response:
        """Provides the list of Test Run Results available for a particular release.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - release_key (Path): Your release id/key
            - status (Query, optional): To get test run results based on the status provided,
                you can get the available status using List Statuses for Test Run api Id [get_statuses_list()]
            - page (Query, optional): Pagination page number

        Returns:
            Response: returns the result of type requests.Response
        """

    # List Test Run Results History
    @get("testRunResults/history/{projectKey}/{testRunKey}/{resultKey}")
    def get_test_run_results_history(
        self,
        project_key: Path("projectKey"),
        test_run_key: Path("testRunKey"),
        result_key: Path("resultKey"),
        page: Query = None,
    ) -> Response:
        """Provides the list of History(s) available of Test Runs Results.

        Args:
            - project_key (Path): Your ID / Project Key / Value
            - test_run_key (Path): Your test run id/key
            - result_key (Path): Your result id/key
            - page (Query, optional): Pagination page number.

        Returns:
            Response: returns the result of type requests.Response
        """

    # List Statuses for Test Run
    @get("testRuns/getAvailableStatuses")
    def get_statuses_list(self) -> Response:
        """Provides the list of available statuses for Test Runs.

        Returns:
            Response: returns the result of type requests.Response
        """

    # Update Test Run Status
    @patch("testRunResults/status")
    def update_test_run_status(
        self,
        status: Query,
        project_key: Query("project"),
        test_run_key: Query("test_run"),
        run_result_key: Query("run_result"),
        comments: Query = None,
        page: Query = None,
    ) -> Response:
        """Update the status for the test run

        Args:
            - status (Query): Status to be updated, one of [Passed, Untested, Blocked, Retest, Failed, Not-applicable, In-progress]
            - project_key (Query): Your project key
            - test_run_key (Query): Your test run key
            - run_result_key (Query): Your run result key
            - comments (Query, optional): Your project key
            - page (Query, optional): Pagination page number

        Returns:
             Response: returns the result of type requests.Response
        """

    # Bulk Update Status for test run
    @patch("bulkupdate")
    def bulk_update_test_runs_status(
        self,
        status: Query,
        project_key: Query("project"),
        test_run_key: Query("test_run"),
        page: Query = None,
    ) -> Response:
        """The test run's all test cases status will be updated at once.

        Args:
            - status (Query): Status to be updated, one of [Passed, Untested, Blocked, Retest, Failed, Not-applicable, In-progress]
            - project_key (Query): Your project key
            - test_run_key (Query): Your test run key
            - page (Query, optional): Pagination page number

        Returns:
             Response: returns the result of type requests.Response
        """

    # List all available Users for Testing
    @get("testRun/availableUsers/{projectKey}")
    def get_available_users_for_project(
        self,
        project_key: Path("projectKey"),
        page: Query = None,
    ) -> Response:
        """Provides the list of Users in the project available for Testing.

        Args:
            - project_key (Path): Your project key
            - page (Query, optional): Pagination page number

        Returns:
             Response: returns the result of type requests.Response
        """

    # Add Test Run Results - Comments and Attachment
    @post("testRunResults/add/results")  # TOdo
    def add_results_to_test_runs(
        self,
        project_key: Query("projectKey"),
        status: Query(),
        test_run: Query(),
        # run_result[]: Query("run_result[]"),
        comments: Query(),
        time_spent: Query = None,
        page: Query = None,
    ) -> Response:
        """Add the result to a specific test run result with comments, time spent and attachments

        Form-Data
        file[]	Uploaded Image

        Args:
            - project_key (Path): Your project key
            - page (Query, optional): Pagination page number

        Returns:
             Response: returns the result of type requests.Response
        """

    # Update Test Run Status

    #
    #
    #

    @post("milestone")
    def create_release(
        self,
        project_key: Query("projectKey"),
        title: Query("milestone"),
        page: Query = None,
    ) -> Response:
        """Create a new Release in your project.

        Args:
            - project_key (Query): Your ID / Project Key / Value under which the Module to be created
            - title (Query): Name of the release to be created
            - page (Query, optional): Pagination page number

        Returns:
            Response: returns the result of type requests.Response
        """


if __name__ == "__main__":
    qatouch = QATouch(
        domain="symbyo",
        api_token="2fbadca221ef193245f5c419646a61e02226f7ec5dda5b232262c5d1e686973b",
    )

    # print(json.dumps(json.loads(qatouch.get_all_projects().content), indent=4))
    # print(qatouch.get_project_summary(project_key="1gEb").url)
    # print(json.dumps(json.loads(qatouch.get_project_summary(project_key="1gEb").content), indent=4))
    # print(json.dumps(json.loads(qatouch.create_new_project(name="test").content), indent=4))
    # print(json.dumps(json.loads(qatouch.get_test_cases_list(project_key="1gEb", view="Count").content),indent=4,))
    # print(json.dumps(json.loads(qatouch.create_new_project(name="test").content), indent=4))
    print(json.dumps(json.loads(qatouch.get_test_modules(project_key="1gEb").content), indent=4))
    print(qatouch.get_test_modules(project_key="1gEb").content)
