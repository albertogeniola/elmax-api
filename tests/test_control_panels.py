"""Test the authentication process."""
import os

import pytest

from elmax_api.exceptions import ElmaxBadLoginError
from elmax_api.http import Elmax


USERNAME = os.environ.get("ELMAX_USERNAME")
PASSWORD = os.environ.get("ELMAX_PASSWORD")


@pytest.mark.asyncio
async def test_list_control_panels():
    client = Elmax(username=USERNAME, password=PASSWORD)
    panels = await client.list_control_panels()
    assert len(panels) > 0
