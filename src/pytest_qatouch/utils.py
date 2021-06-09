QATOUCH_API_END_POINT = "https://api.qatouch.com/api/v1"

# From https://github.com/gitdckap/cypress-qatouch-reporter/blob/main/dist/qatouch.js

TEST_CASE_STATUS = {
    "passed": 1,
    "skipped": 3,  # 3 represent blocked in qatouch
    "failed": 5,
}

QATOUCH_MARK = "qatouch"


class WrongQatouchStatus(Exception):
    """Exception for passing a wrong test cases status"""

    pass


class MissingQatouchData(Exception):
    """Exception for passing a wrong test cases status"""

    pass


class ExpectedIntegerValue(Exception):
    """Exception for passing non integer value"""

    pass


class QatouchRequestError(Exception):
    """Exception for faild requests"""

    pass
