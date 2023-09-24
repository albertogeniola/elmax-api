import asyncio
import json
import logging
import ssl
from asyncio import FIRST_COMPLETED, Event

import websockets

from elmax_api.http import GenericElmax
from elmax_api.model.panel import PanelStatus

_LOGGER = logging.getLogger(__name__)
_ERROR_WAIT_PERIOD = 15


class PushNotificationHandler:

    def __init__(self, endpoint: str, http_client: GenericElmax, ssl_context: ssl.SSLContext = None):
        self._endpoint = endpoint
        self._client = http_client
        self._event_handlers = set()
        if ssl_context is None:
            self._ssl_context = ssl.create_default_context()
        else:
            self._ssl_context = ssl_context
        self._should_run = False
        self._task = None
        self._loop = None
        self._stop_event = Event()

    def register_push_notification_handler(self, coro):
        if coro not in self._event_handlers:
            self._event_handlers.add(coro)

    def unregister_push_notification_handler(self, coro):
        if coro in self._event_handlers:
            self._event_handlers.remove(coro)

    def start(self, loop):
        self._stop_event.clear()
        self._should_run = True
        self._loop = loop
        self._task = loop.create_task(self._looper())

    def stop(self):
        self._should_run = False
        self._stop_event.set()

    async def _connect(self):
        token = await self._client.login()
        return await websockets.connect(self._endpoint, ssl=self._ssl_context, extra_headers={
            "Authorization": self._client._raw_jwt
        })

    async def _notify_handlers(self, message):
        _LOGGER.debug("Handling message dispatching for handlers")
        message_dict = json.loads(message)
        status = PanelStatus.from_api_response(message_dict)
        _LOGGER.debug("Parsed panel-status: %s", status)
        _LOGGER.debug("There are %d registered event handlers.", len(self._event_handlers))
        for coro in self._event_handlers:
            try:
                _LOGGER.debug("Dispatching to event handler %s.", str(coro))
                await coro(status)
            except Exception as e:
                _LOGGER.exception("Error occurred when notifying a push-notification handler")

    async def _wait_for_messages(self, connection):
        while self._should_run:
            stop_event_waiter = self._loop.create_task(self._stop_event.wait())
            receive_waiter = self._loop.create_task(connection.recv())
            done, pending = await asyncio.wait([receive_waiter, stop_event_waiter], return_when=FIRST_COMPLETED)
            if stop_event_waiter in done:
                _LOGGER.info("Push notification handler has received stop signal. Aborting wait for messages...")
                receive_waiter.cancel()
                return
            message = receive_waiter.result()
            _LOGGER.debug("Push notification message received from websocket: %s", str(message))
            await self._notify_handlers(message)

    async def _looper(self):
        while self._should_run:
            _LOGGER.debug("Push Notification looper has started.")
            try:
                connection = await self._connect()
                _LOGGER.debug("Push Notification looper has connected successfully to the websocket. Waiting for messages...")
                await self._wait_for_messages(connection)
            except Exception as e:
                _LOGGER.exception("Error occurred when handling websocket connection. We will re-establish the "
                                  "connection in %d seconds.", _ERROR_WAIT_PERIOD)
                await asyncio.sleep(_ERROR_WAIT_PERIOD, loop=self._loop)

