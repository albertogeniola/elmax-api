"""Test the authentication process."""
import os

import pytest

from elmax_api.http import Elmax
from elmax_api.model.actuator import Actuator
from elmax_api.model.area import Area
from elmax_api.model.goup import Group
from elmax_api.model.panel import PanelStatus
from elmax_api.model.scene import Scene
from elmax_api.model.zone import Zone

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
    status = await client.get_panel_status(control_panel_id=panel.hash) # type: PanelStatus
    assert isinstance(status, PanelStatus)

    # Make sure the username matches the one used by the client
    assert status.user_email == USERNAME
    assert status.panel_id == panel.hash


@pytest.mark.asyncio
async def test_single_device_status():
    client = Elmax(username=USERNAME, password=PASSWORD)
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first panel
    panel = online_panels[0]

    # Retrieve its status
    status = await client.get_panel_status(control_panel_id=panel.hash)  # type: PanelStatus
    assert isinstance(status, PanelStatus)

    # Make sure we can read each status correctly
    for endpoint in status.all_endpoints:
        epstatus = await client.get_endpoint_status(endpoint_id=endpoint.endpoint_id)

        if isinstance(endpoint, Actuator):
            assert epstatus.actuators[0] == endpoint
        elif isinstance(endpoint, Area):
            assert epstatus.areas[0] == endpoint
        elif isinstance(endpoint, Group):
            assert epstatus.groups[0] == endpoint
        elif isinstance(endpoint, Scene):
            assert epstatus.scenes[0] == endpoint
        elif isinstance(endpoint, Zone):
            assert epstatus.zones[0] == endpoint
        else:
            raise ValueError("Unexpected/unhandled endpoint")
