"""Test the actuator functionalities."""
import asyncio

import pytest

from elmax_api.exceptions import ElmaxBadPinError, ElmaxPanelBusyError, ElmaxApiError
from elmax_api.http import Elmax
from elmax_api.model.alarm_status import AlarmStatus, AlarmArmStatus
from elmax_api.model.area import Area
from elmax_api.model.command import Command, AreaCommand
from elmax_api.model.panel import PanelStatus, PanelEntry
from tests import USERNAME, PASSWORD


client = Elmax(username=USERNAME, password=PASSWORD)
entry = None  # type:PanelEntry

def setup_module(module):
    global entry
    print ("This will at start of module")

    panels = asyncio.run(client.list_control_panels())
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first online panel
    entry = online_panels[0]  # type:PanelEntry


async def get_area():
    # Retrieve current area status
    panel = await client.get_panel_status(control_panel_id=entry.hash)
    assert isinstance(panel, PanelStatus)
    assert len(panel.areas) > 0
    # Do not work with un-armable areas
    a = filter(lambda x: x.status != AlarmStatus.NOT_ARMED_NOT_ARMABLE, panel.areas)
    return list(a)[0]


async def reset_area_status(area: Area, command: AreaCommand, expected_arm_status: AlarmArmStatus, code: str = "000000") -> Area:
    res = await client.execute_command(endpoint_id=area.endpoint_id, command=command, extra_payload={"code": code})

    attempts = 0
    while attempts < 3:
        # Make sure the area is now consistent
        status = await client.get_endpoint_status(endpoint_id=area.endpoint_id)
        area = status.areas[0]

        if area.armed_status != expected_arm_status:
            attempts += 1
            await asyncio.sleep(delay=2.0)
        else:
            return area
    pytest.fail(f"RESET_AREA_STATUS failed to set status {expected_arm_status} on area {area}")


@pytest.mark.asyncio
async def test_area_wrong_disarm_code():
    # Make sure the area is disarmed
    area = await get_area()
    if area.armed_status != AlarmArmStatus.NOT_ARMED:
        await reset_area_status(area=area, command=AreaCommand.DISARM, expected_arm_status=AlarmArmStatus.NOT_ARMED)

    # ARM TOTALLY
    area = await get_area()
    area = await reset_area_status(area=area, command=AreaCommand.ARM_TOTALLY, expected_arm_status=AlarmArmStatus.ARMED_TOTALLY)

    # Check status
    assert area.status == AlarmStatus.ARMED_STANDBY

    # Disarm with wrong code
    error403 = False
    try:
        area = await reset_area_status(area=area, command=AreaCommand.DISARM, expected_arm_status=AlarmArmStatus.NOT_ARMED, code="999999")
    except ElmaxApiError as e:
        error403 = e.status_code == 403

    if not error403:
        pytest.fail("Expected ERROR 403, but it hasn't occurred")

    assert area.status == AlarmStatus.ARMED_STANDBY


@pytest.mark.asyncio
async def test_area_arming_totally():
    # Make sure the area is disarmed
    area = await get_area()
    if area.armed_status != AlarmArmStatus.NOT_ARMED:
        await reset_area_status(area=area, command=AreaCommand.DISARM, expected_arm_status=AlarmArmStatus.NOT_ARMED)

    # ARM TOTALLY
    area = await get_area()
    area = await reset_area_status(area=area, command=AreaCommand.ARM_TOTALLY, expected_arm_status=AlarmArmStatus.ARMED_TOTALLY)

    # Check status
    assert area.status == AlarmStatus.ARMED_STANDBY


@pytest.mark.asyncio
async def test_area_disarm():
    # Make sure the area is armed first
    area = await get_area()
    if area.armed_status != AlarmArmStatus.ARMED_TOTALLY:
        await reset_area_status(area=area, command=AreaCommand.ARM_TOTALLY, expected_arm_status=AlarmArmStatus.ARMED_TOTALLY)

    # DISARM
    area = await get_area()
    area = await reset_area_status(area=area, command=AreaCommand.DISARM,
                                   expected_arm_status=AlarmArmStatus.NOT_ARMED)

    # Check status
    assert area.status in (AlarmStatus.NOT_ARMED_NOT_TRIGGERED, AlarmStatus.NOT_ARMED_NOT_ARMABLE)
