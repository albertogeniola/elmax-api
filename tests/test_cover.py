"""Test the actuator functionalities."""
import asyncio

import pytest

from elmax_api.http import Elmax
from elmax_api.model.command import Command
from elmax_api.model.cover_status import CoverStatus
from elmax_api.model.panel import PanelStatus, PanelEntry
from tests import USERNAME, PASSWORD


@pytest.mark.asyncio
async def test_open_close():
    client = Elmax(username=USERNAME, password=PASSWORD)
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first online panel
    entry = online_panels[0]  # type:PanelEntry

    # Do this twice so we toggle every cover up->down and down ->up
    for i in range(2):
        # Retrieve its status
        panel = await client.get_panel_status(control_panel_id=entry.hash)  # type: PanelStatus
        assert isinstance(panel, PanelStatus)

        # Store old status into a dictionary for later comparison
        cover_status = { cover.endpoint_id: cover.status for cover in panel.covers}
        cover_position = { cover.endpoint_id: cover.position for cover in panel.covers}

        # Toggle all the actuators
        for endpoint_id, curr_status in cover_position.items():
            command = Command.UP if curr_status==0 else Command.DOWN
            await client.execute_command(endpoint_id=endpoint_id, command=command)

        # Ensure all the actuators switched correctly
        await asyncio.sleep(15)
        panel = await client.get_panel_status(control_panel_id=entry.hash)  # type: PanelStatus

        for cover in panel.covers:
            expected_position = 100 if cover_position[cover.endpoint_id] == 0 else 0
            assert cover.position==expected_position

@pytest.mark.asyncio
async def test_up_down_states():
    client = Elmax(username=USERNAME, password=PASSWORD)
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first online panel
    entry = online_panels[0]  # type:PanelEntry

    # Do this twice so we toggle every cover up->down and down ->up
    for i in range(2):
        # Retrieve its status
        panel = await client.get_panel_status(control_panel_id=entry.hash)  # type: PanelStatus
        assert isinstance(panel, PanelStatus)

        # Store old status into a dictionary for later comparison
        cover_position = {cover.endpoint_id: cover.position for cover in panel.covers}

        # Toggle all the actuators
        for endpoint_id, curr_status in cover_position.items():
            command = Command.UP if curr_status==0 else Command.DOWN
            await client.execute_command(endpoint_id=endpoint_id, command=command)
            cover_status = {cover.endpoint_id: cover.status for cover in panel.covers}
            panel = await client.get_panel_status(control_panel_id=entry.hash)  # type: PanelStatus
            assert cover_status[endpoint_id] == CoverStatus.DOWN if command == Command.DOWN else CoverStatus.UP
