"""Test the authentication process."""
import os

import pytest

from elmax_api.exceptions import ElmaxBadLoginError
from elmax_api.http import Elmax

BAD_USERNAME = "thisIsWrong@gmail.com"
BAD_PASSWORD = "fakePassword"
GOOD_USERNAME = os.environ.get("ELMAX_USERNAME")
GOOD_PASSWORD = os.environ.get("ELMAX_PASSWORD")


@pytest.mark.asyncio
async def test_wrong_credentials():
    client = Elmax(username=BAD_USERNAME, password=BAD_PASSWORD)
    with pytest.raises(ElmaxBadLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_good_credentials():
    client = Elmax(username=GOOD_USERNAME, password=GOOD_PASSWORD)
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)
