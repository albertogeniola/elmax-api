"""Constants for the Elmax Cloud service client."""

from . import __version__


# URL Constants
# TODO: uncomment the following
# BASE_URL = "https://cloud.elmaxsrl.it"
BASE_URL = "https://test.fabiozingaro.com"
ENDPOINT_DEVICES = "api/ext/devices"
# TODO: Seems not the corrent one
# ENDPOINT_LOGIN = "api/ext/login"
ENDPOINT_LOGIN = "api/auth/login"
ENDPOINT_STATUS_ENTITY_ID = "api/ext/status"
ENDPOINT_ENTITY_ID_COMMAND = "api/ext"
ENDPOINT_DISCOVERY = "api/ext/discovery"

# User agent
USER_AGENT = f"elmax-api/{__version__}"

# Command constants
COMMAND_ON = "on"
COMMAND_OFF = "off"
COMMAND_ARM = "ins"
COMMAND_DISARM = "dis"

# Model constants
ZONE = "zone"
OUTPUT = "uscite"
AREA = "aree"
UNIT_TYPES = [
    AREA,
    OUTPUT,
    ZONE,
]
