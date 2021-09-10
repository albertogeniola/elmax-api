import asyncio
import functools
import logging
import time
from enum import Enum
from typing import Dict, List, Optional

import httpx
import jwt
from yarl import URL

from elmax_api.constants import BASE_URL, ENDPOINT_LOGIN, USER_AGENT, ENDPOINT_DEVICES
from elmax_api.exceptions import ElmaxBadLoginError, ElmaxApiError, ElmaxNetworkError
from elmax_api.model.panel import ControlPanel
from elmax_api.model.registry import DeviceRegistry

_LOGGER = logging.getLogger(__name__)
_JWT_ALGS = ["HS256"]


def async_auth(func,
               *method_args,
               **method_kwargs):
    """
    Asynchronous decorator used to check validity of JWT token.
    It takes care to verify the validity of a JWT token before issuing the method call.
    In case the JWT is expired, or close to expiration date, it tries to renew it.
    """

    async def helper(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    @functools.wraps(func,
                     *method_args,
                     **method_kwargs)
    async def wrapper(*args, **kwargs):
        # Check whether the client has a valid token to be used. We consider valid tokens with expiration time
        # > 10minutes. If not, try to login first and then proceed with the function call.
        now = time.time()
        _instance = args[0]
        assert isinstance(_instance, Elmax)
        if (_instance.token_expiration_time - now) < 600:
            _LOGGER.info("The API was not authorized yet or the token is going to be expired soon. "
                         "The token will be refreshed now.")
            await _instance.login()
        # At this point, we assume the client has a valid token to use for authorized APIs. So let's use it.
        result = await helper(func, *args, **kwargs)
        return result

    return wrapper


class Elmax(object):
    """A class for handling the data retrieval."""

    def __init__(
            self,
            username: str,
            password: str
    ):
        """Initialize the connection.

        Args:
            username: Username to use for Elmax Authentication
            password: Password to use for Elmax Authentication
        """
        self._username = username
        self._password = password
        self._raw_jwt = None
        self._jwt = None
        self._areas = self._outputs = self._zones = []

        self.registry = DeviceRegistry()

    async def _request(self,
                       method: 'Elmax.HttpMethod',
                       url: str,
                       data: Optional[Dict] = None,
                       authorized: bool = False) -> Dict:
        """
        Executes a HTTP API request against a given endpoint, parses the output and returns the
        json to the caller. It handles most basic IO exceptions.
        If the API returns a non 200 response, this method raises an `ElmaxApiError`

        Args:
            method: HTTP method to use for the HTTP request
            url: Target request URL
            data: Json data/Data to post in POST messages. Ignored when issuing GET requests
            authorized: When set, the request is performed passing the stored authorization token

        Returns:
            Dict: The dictionary object containing authenticated JWT data

        Raises:
            ElmaxApiError: Whenever a non 200 return code is returned by the remote server
            ElmaxNetworkError: If the http request could not be completed due to a network error
        """
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if authorized:
            headers["Authorization"] = f"JWT {self._raw_jwt}"

        try:
            async with httpx.AsyncClient() as client:
                if method == Elmax.HttpMethod.GET:
                    response = await client.get(str(url), headers=headers)
                elif method == Elmax.HttpMethod.POST:
                    response = await client.post(str(url), headers=headers, json=data)
                else:
                    raise ValueError("Invalid/Unhandled method. Expecting GET or POST")

                _LOGGER.debug(f"HTTP Request %s %s -> Status code: %d", str(method), url, response.status_code)
                if response.status_code != 200:
                    _LOGGER.error("Api call failed. Method=%s, Url=%s, Data=%s. Response code=%d. Response content=%s",
                                  method,
                                  url,
                                  str(data),
                                  response.status_code,
                                  str(response.content))
                    raise ElmaxApiError(status_code=response.status_code)
                return response.json()

        # Wrap any other HTTP/NETWORK error
        except httpx.ConnectError as e:
            _LOGGER.exception("An unhandled error occurred while executing API Call.")
            raise ElmaxNetworkError(f"A network error occurred")

    @property
    def is_authenticated(self) -> bool:
        """
        Specifies whether the client has been granted a JWT which is still valid (not expired)

        Returns:
            bool: True if there is a valid JWT token, False if there's no token or if it is expired
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
        """
        Returns the expiration timestamp of the stored JWT token.

        Returns:
            int: The timestamp of expiration or -1 if no token was present.
        """
        if self._jwt is None:
            return 0
        return self._jwt.get("exp", -1)

    @async_auth
    async def logout(self) -> None:
        """
        Invalidate the current token

        TODO:
            * Check if there is a HTTP API to invalidate the current token
        """
        self._jwt = None

    async def login(self) -> Dict:
        """
        Connects to the API ENDPOINT and returns the access token to be used within the client

        Raises:
            ElmaxBadLoginError: if the login attempt fails due to bad username/password credentials
            ValueError: in case the json response is malformed
        """
        url = URL(BASE_URL) / ENDPOINT_LOGIN
        data = {
            "username": self._username,
            "password": self._password,
        }
        try:
            response_data = await self._request(method=Elmax.HttpMethod.POST, url=url, data=data, authorized=False)
        except ElmaxApiError as e:
            if e.status_code == 401:
                raise ElmaxBadLoginError()
            raise

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

    @async_auth
    async def list_control_panels(self) -> List[ControlPanel]:
        """
        Lists the control panels available for the given user

        Returns:
            List[ControlPanel]: The list of fetched `ControlPanel` devices discovered via the API
        """
        res = []
        url = URL(BASE_URL) / ENDPOINT_DEVICES

        response_data = await self._request(method=Elmax.HttpMethod.GET, url=url, authorized=True)
        for response_entry in response_data:
            res.append(ControlPanel.from_api_response(response_entry))
        return res

    class HttpMethod(Enum):
        """Enumerative helper for supported HTTP methods of the Elmax API"""
        GET = 'get'
        POST = 'post'

    """
    @async_auth
    async def get_endpoints(self, control_panel_id, pin):
        url = URL(BASE_URL) / ENDPOINT_DISCOVERY / control_panel_id / str(pin)
        headers["Authorization"] = f"JWT {self._raw_jwt}"

        async with httpx.AsyncClient() as client:
            response = await client.get(str(url), headers=headers)

        response_data = response.json()

        if response_data[ZONE]:
            self._zones = response_data[ZONE]
        if response_data[OUTPUT]:
            self._outputs = response_data[OUTPUT]
        if response_data[AREA]:
            self._areas = response_data[AREA]
    """

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
