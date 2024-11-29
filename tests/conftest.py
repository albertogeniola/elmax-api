import asyncio

import pytest

from elmax_api.http import ElmaxLocal, Elmax
from tests import LOCAL_TEST, USERNAME, PASSWORD, LOCAL_API_URL, PANEL_PIN, ONLINE_PANEL_ID


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def async_init_test() -> Elmax:
    client = Elmax(username=USERNAME, password=PASSWORD) if not LOCAL_TEST else ElmaxLocal(panel_api_url=LOCAL_API_URL,
                                                                                           panel_code=PANEL_PIN)
    if not LOCAL_TEST:
        panels = await client.list_control_panels()
        online_panels = list(filter(lambda x: x.online, panels))
        assert len(online_panels) > 0

        if ONLINE_PANEL_ID is not None:
            online_panels = list(filter(lambda x: x.hash == ONLINE_PANEL_ID, online_panels))

        # Select the first online panel
        entry = online_panels[0]  # type:PanelEntry
        client.set_current_panel(panel_id=entry.hash)

    return client

async def async_init_test_cover() -> Elmax:
    client = Elmax(username=USERNAME, password=PASSWORD) if not LOCAL_TEST else ElmaxLocal(panel_api_url=LOCAL_API_URL,
                                                                                           panel_code=PANEL_PIN)
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    if ONLINE_PANEL_ID is not None:
        online_panels = list(filter(lambda x: x.hash == ONLINE_PANEL_ID, online_panels))

    # Select the first online panel which has covers
    panel_found = False
    for panel in online_panels:
        panel_status = await client.get_panel_status(panel.hash)
        if len(panel_status.covers) > 0:
            panel_found = True
            client.set_current_panel(panel_id=panel.hash)
            break

    if not panel_found:
        pytest.skip("No panel found to run this test set.")

    return client