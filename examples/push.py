import asyncio
import ssl

from elmax_api.http import ElmaxLocal
from elmax_api.model.panel import PanelStatus
from elmax_api.push.push import PushNotificationHandler


async def main():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.VerifyMode(ssl.CERT_NONE)
    client = ElmaxLocal(panel_api_url="https://192.168.7.249/api/v2", panel_code="000000", ssl_context=context)
    handler = PushNotificationHandler("wss://192.168.7.249/api/v2/push", client, context)

    async def _panel_updated(status: PanelStatus):
        print(status)

    handler.register_push_notification_handler(_panel_updated)
    handler.start(asyncio.get_event_loop())

    for i in range(60):
        await asyncio.sleep(1)
        print("Slept!")

    handler.stop()

if __name__ == '__main__':
    asyncio.run(main())


