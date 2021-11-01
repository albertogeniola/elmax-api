"""Test the authentication process."""

import pytest

from elmax_api.exceptions import ElmaxBadLoginError
from elmax_api.http import Elmax
from tests import PASSWORD, USERNAME

BAD_USERNAME = "thisIsWrong@gmail.com"
BAD_PASSWORD = "fakePassword"


@pytest.mark.asyncio
async def test_wrong_credentials():
    client = Elmax(username=BAD_USERNAME, password=BAD_PASSWORD)
    with pytest.raises(ElmaxBadLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_good_credentials():
    client = Elmax(username=USERNAME, password=PASSWORD)
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)

    username = client.get_authenticated_username()
    assert username == USERNAME
