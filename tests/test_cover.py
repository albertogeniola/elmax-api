"""Test the actuator functionalities."""
import asyncio

import pytest

from elmax_api.http import Elmax
from elmax_api.model.command import Command
from elmax_api.model.cover import Cover
from elmax_api.model.cover_status import CoverStatus
from elmax_api.model.panel import PanelStatus, PanelEntry
from tests import USERNAME, PASSWORD
import time


async def wait_for_cover_status(client: Elmax, endpoint_id: str, status: CoverStatus, timeout: float) -> bool:
    t = time.time()
    deadline = t + timeout

    while time.time() < deadline:
        try:
            cur_status = await client.get_endpoint_status(endpoint_id=endpoint_id)
            cover: Cover = cur_status.covers[0]
            if cover.status == status:
                return True
        finally:
            await asyncio.sleep(delay=2)
    return False


async def wait_for_cover_position(client: Elmax, endpoint_id: str, position: int, timeout: float) -> bool:
    t = time.time()
    deadline = t + timeout

    while time.time() < deadline:
        try:
            cur_status = await client.get_endpoint_status(endpoint_id=endpoint_id)
            cover: Cover = cur_status.covers[0]
            if cover.position == position:
                return True
        finally:
            await asyncio.sleep(delay=2)
    raise TimeoutError()


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
        cover_position = { cover.endpoint_id: cover.position for cover in panel.covers}

        # Toggle all the actuators
        tasks = []
        for endpoint_id, curr_status in cover_position.items():
            command = Command.UP if curr_status==0 else Command.DOWN
            await client.execute_command(endpoint_id=endpoint_id, command=command)
            expected_position = 100 if command==Command.UP else 0
            t = wait_for_cover_position(client=client, endpoint_id=endpoint_id, position=expected_position, timeout=20.0)
            tasks.append(t)

        # Ensure all the actuators switched correctly
        done, pending = await asyncio.wait(tasks, return_when="FIRST_EXCEPTION")
        for t in done:
            if t.exception():
                pytest.fail("One of the covers failed")
                t.cancel()


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
        tasks = []
        for endpoint_id, curr_status in cover_position.items():
            command = Command.UP if curr_status==0 else Command.DOWN
            await client.execute_command(endpoint_id=endpoint_id, command=command)
            expected_status = CoverStatus.UP if command == Command.UP else CoverStatus.DOWN
            t = wait_for_cover_status(client=client, endpoint_id=endpoint_id, status=expected_status,timeout=4.0)
            tasks.append(t)

        # Ensure all the actuators switched correctly
        done, pending = await asyncio.wait(tasks, return_when="FIRST_EXCEPTION")
        for t in done:
            if t.exception():
                pytest.fail("One of the covers failed")
                t.cancel()
