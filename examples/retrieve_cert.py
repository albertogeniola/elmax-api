import asyncio
import os
import ssl

from elmax_api.http import  ElmaxLocal
from elmax_api.model.command import SwitchCommand

LOCAL_PANEL_IP = "192.168.1.139"
LOCAL_PANEL_PORT = 8443


async def main():
    # Instantiate the Elmax API client
    cert = await ElmaxLocal.retrieve_server_certificate(hostname=LOCAL_PANEL_IP, port=LOCAL_PANEL_PORT)
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = False
    # We only load a very specific CA certificate
    ssl_context.load_verify_locations(cadata=cert)

    client = ElmaxLocal(panel_api_url=f"https://{LOCAL_PANEL_IP}:{LOCAL_PANEL_PORT}/api/v2", panel_code="000000", ssl_context=ssl_context)
    status = await client.get_current_panel_status()
    print(f"Status: {status}")


if __name__ == '__main__':
    asyncio.run(main())