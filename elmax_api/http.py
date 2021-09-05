import logging
import time
from functools import wraps
from typing import Dict
import decorator

import httpx
import jwt
from yarl import URL

from elmax_api import exceptions
from elmax_api.constants import BASE_URL, ENDPOINT_LOGIN, USER_AGENT, ENDPOINT_DEVICES
from elmax_api.exceptions import ElmaxBadLoginError, ElmaxError
from elmax_api.model.registry import DeviceRegistry

_LOGGER = logging.getLogger(__name__)
_JWT_ALGS = ["HS256"]
headers = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}


@decorator.decorator
async def async_auth(coro,
                     self,  # type: Elmax
                     *method_args,
                     **method_kwargs):
    # Check whether the client has a valid token to be used. We consider valid tokens with expiration time
    # > 10minutes. If not, try to login first and then proceed with the function call.
    now = time.time()
    if (self.token_expiration_time - now) < 600:
        _LOGGER.info("The API was not authorized yet or the token is going to be expired soon. "
                     "The token will be refreshed now.")
        await self.login()

    # At this point, we assume the client has a valid token to use for authorized APIs. So let's use it.
    method_output = await coro(self, *method_args, **method_kwargs)
    return method_output


class Elmax(object):
    """A class for handling the data retrieval."""

    def __init__(
            self,
            username: str,
            password: str,
            control_panel_id: str = None
    ):
        """Initialize the connection."""
        self.control_panel_id = control_panel_id
        self._username = username
        self._password = password
        self._raw_jwt = None
        self._jwt = None
        self._areas = self._outputs = self._zones = []

        self.registry = DeviceRegistry()

    async def login(self) -> Dict:
        """
        Connects to the API ENDPOINT and returns the access token to be used within the client
        """
        url = URL(BASE_URL) / ENDPOINT_LOGIN
        data = {
            "username": self._username,
            "password": self._password,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(str(url), headers=headers, json=data)
                _LOGGER.debug("Login Status code:", response.status_code)
                if response.status_code != 200:
                    # Login failed
                    _LOGGER.error("Login failed. Status code was %d.", response.status_code)
                    raise ElmaxBadLoginError()

                response_data = response.json()
                if "token" not in response_data:
                    raise ValueError("Missing token parameter in json response")

                jwt_token = response_data["token"]
                if not jwt_token.startswith("JWT "):
                    raise ValueError("API did not return JWT token as expected")
                jt = jwt_token.split("JWT ")[1]

                # We do not need to verify the signature as this is usually something the server
                # needs to do. We will just decode it to get information about user/claims.
                # Moreover, since the JWT is obtained over a HTTPS channel, we do not need to verify
                # its integrity/confidentiality as the ssl does this for us
                self._jwt = jwt.decode(jt, algorithms=_JWT_ALGS, options={"verify_signature": False})
                self._raw_jwt = jt  # keep an encoded version of the JWT for convenience and performance
                return self._jwt

        # Let the caller handle/recover from these exceptions
        except ElmaxError as e:
            raise

        # Wrap any other HTTP/NETWORK error
        except httpx.ConnectError as e:
            _LOGGER.exception("An unhandled error occurred while logging in")
            raise exceptions.ElmaxError(f"Login to {BASE_URL} failed")

    def is_authenticated(self) -> bool:
        """
        Returns whether the client has been granted a JWT which is still valid (not expired)
        """
        if self._jwt is None:
            # The user did not login yet
            return False
        if self._jwt.get("exp", 0) <= time.time():
            self._jwt = None
            return False
        return True

    @property
    def token_expiration_time(self) -> int:
        if self._jwt is None:
            return 0
        return self._jwt.get("exp", 0)

    @async_auth
    async def logout(self):
        """
        Invalidate the current token
        """
        # TODO: is there any API to call to invalidate a token?
        self._jwt = None

    @async_auth
    async def list_control_panels(self):
        """
        Lists the control panels available for the given user
        """
        url = URL(BASE_URL) / ENDPOINT_DEVICES
        headers["Authorization"] = f"JWT {self._raw_jwt}"

        async with httpx.AsyncClient() as client:
            response = await client.get(str(url), headers=headers)

        _LOGGER.debug("List-Control-Panels Status code:", response.status_code)
        for response_entry in response.json():
            control_panel = ControlPanel.from_api_response(response_entry)
            self.registry.register(control_panel)

        # TODO: unregister old panels that are no more available

    # async def list_control_panels(self):
    #     """List all available control panels."""
    #     await self.get_control_panels()
    #
    #     control_panels_list = []
    #     for control_panel in self.registry.devices():
    #         control_panels_list.append(
    #             {
    #                 "online": control_panel.online,
    #                 "hash": control_panel.hash,
    #                 "name": control_panel.name,
    #             }
    #         )
    #
    #     return control_panels_list
    #
    # async def get_endpoints(self, control_panel_id, pin):
    #     """List all endpoints of a control panel."""
    #     if self.authorized is False:
    #         await self.connect()
    #
    #     url = URL(BASE_URL) / ENDPOINT_DISCOVERY / control_panel_id / str(pin)
    #
    #     headers["Authorization"] = self.authorization
    #
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(str(url), headers=headers)
    #
    #     response_data = response.json()
    #
    #     if response_data[ZONE]:
    #         self._zones = response_data[ZONE]
    #     if response_data[OUTPUT]:
    #         self._outputs = response_data[OUTPUT]
    #     if response_data[AREA]:
    #         self._areas = response_data[AREA]
    #
    # async def get_status(self, endpoint_id):
    #     """Get the status of an endpoint."""
    #     if self.authorized is False:
    #         self.connect()
    #
    #     url = URL(BASE_URL) / ENDPOINT_STATUS_ENTITY_ID / endpoint_id
    #
    #     headers["Authorization"] = self.authorization
    #
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(str(url), headers=headers)
    #
    #     return response.json()
