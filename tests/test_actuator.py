"""Test the actuator functionalities."""
import asyncio

import pytest

from elmax_api.http import Elmax
from elmax_api.model.command import SwitchCommand
from elmax_api.model.panel import PanelStatus, PanelEntry
from tests import USERNAME, PASSWORD


@pytest.mark.asyncio
async def test_device_command():
    client = Elmax(username=USERNAME, password=PASSWORD)
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first online panel
    entry = online_panels[0]  # type:PanelEntry

    # Retrieve its status
    panel = await client.get_panel_status(control_panel_id=entry.hash)  # type: PanelStatus
    assert isinstance(panel, PanelStatus)

    # Store old status into a dictionary for later comparison
    actuator_status = { actuator.endpoint_id:actuator.opened for actuator in panel.actuators}

    # Toggle all the actuators
    for endpoint_id, curr_status in actuator_status.items():
        command = SwitchCommand.TURN_OFF if curr_status else SwitchCommand.TURN_ON
        await client.execute_command(endpoint_id=endpoint_id, command=command)

    # Ensure all the actuators switched correctly
    await asyncio.sleep(3)
    panel = await client.get_panel_status(control_panel_id=entry.hash)  # type: PanelStatus

    for actuator in panel.actuators:
        expected_status = not actuator_status[actuator.endpoint_id]
        assert actuator.opened == expected_status

    # Restore original status
    for endpoint_id, curr_status in actuator_status.items():
        command = SwitchCommand.TURN_ON if curr_status else SwitchCommand.TURN_OFF
        await client.execute_command(endpoint_id=endpoint_id, command=command)
