"""Constants for the Elmax Cloud service client."""

from . import __version__


# URL Constants
BASE_URL = "https://cloud.elmaxsrl.it/api/ext/"
ENDPOINT_DEVICES = "devices"
ENDPOINT_LOGIN = "login"
ENDPOINT_STATUS_ENTITY_ID = "status"
ENDPOINT_DISCOVERY = "discovery"
ENDPOINT_LOCAL_CMD = "cmd"

# User agent
USER_AGENT = f"elmax-api/{__version__}"

# DEFAULT HTTP TIMEOUT
DEFAULT_HTTP_TIMEOUT = 20.0
BUSY_WAIT_INTERVAL = 2.0



