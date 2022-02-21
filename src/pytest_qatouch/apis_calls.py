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


import asyncio
import aiohttp
import re, json, time
from aiolimiter import AsyncLimiter

ref = time.time()


async def get_tcs(session, limiter, url, page_num, headers, get_lastlink=False):
    await asyncio.sleep(page_num * 0.01)
    async with limiter:
        print(f"{page_num:>2d}: Drip! {time.time() - ref:>5.2f}")
        async with session.get(f"{url}&page={page_num}", headers=headers) as response:
            if response.status == 200:
                res = await response.json()
                if res.get("data"):
                    tc_keys = []
                    for tc in res.get("data"):
                        tc_keys.append(tc["case_key"])

                    # print(f"\nThe qatouch request updated test run successfully {json.dumps(res)}")
                    if get_lastlink:
                        return tc_keys, res["link"]["last"]
                    else:
                        return tc_keys

                else:
                    raise QatouchRequestError(f"The qatouch request failed with {[res.get('msg')]}")

            else:
                raise QatouchRequestError(
                    f"""Expected to have 200 for the qatoch request but got {response.status},
                            Please make sure the specified domain and API token are right."""
                )


async def get_all_tcs(limiter, url, headers):
    pagination_pages = 1
    async with aiohttp.ClientSession() as session:
        first_tcs_keys, link = await get_tcs(session, limiter, url, 1, headers, get_lastlink=True)
        pagination_pages = int(re.search("(?<=page\\=)\\d+", link).group())
        print(pagination_pages)
        if pagination_pages == 1:
            return first_tcs_keys

        tasks = [get_tcs(session, limiter, url, i, headers) for i in range(2, pagination_pages + 1)]
        groups = await asyncio.gather(*tasks)
        tcs_keys = first_tcs_keys
        for group in groups:
            tcs_keys = tcs_keys + group

        return tcs_keys


def get_qatouch_tcs_key(url, headers):
    limiter = AsyncLimiter(max_rate=4, time_period=15)
    return asyncio.get_event_loop().run_until_complete(get_all_tcs(limiter, url, headers))


URL = "https://api.qatouch.com/api/v1/getAllTestCases/3b9e/?mode=Automation"  # 3b9e   1gEb
HEADERS = {
    "domain": "symbyo",
    "api-token": "476cf2ffc41704a3f222bb1092445d6cabe107d012e442c85c55e1b1424994bc",
}
print(get_qatouch_tcs_key(URL, HEADERS))
