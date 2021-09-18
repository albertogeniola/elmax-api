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


@pytest.mark.asyncio
async def test_get_control_panel_status():
    client = Elmax(username=USERNAME, password=PASSWORD)
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first panel
    panel = online_panels[0]

    # Retrieve its status
    status = await client.get_panel_status(control_panel_id=panel.hash)
