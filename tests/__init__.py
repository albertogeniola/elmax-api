"""Test for the Elmax Cloud service client."""
import os

from elmax_api.http import Elmax, ElmaxLocal

USERNAME = os.environ.get("ELMAX_USERNAME")
PASSWORD = os.environ.get("ELMAX_PASSWORD")
PANEL_PIN = os.environ.get("ELMAX_PANEL_PIN")
LOCAL_TEST = os.environ.get("LOCAL_TEST", "false")
LOCAL_API_URL = os.environ.get("LOCAL_API_URL")

LOCAL_TEST = LOCAL_TEST.lower() == "true"
client = Elmax(username=USERNAME, password=PASSWORD) if not LOCAL_TEST else ElmaxLocal(panel_api_url=LOCAL_API_URL, panel_code=PANEL_PIN)