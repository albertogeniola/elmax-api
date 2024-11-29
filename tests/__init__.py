"""Test for the Elmax Cloud service client."""
import os

USERNAME = os.environ.get("ELMAX_USERNAME")
PASSWORD = os.environ.get("ELMAX_PASSWORD")
PANEL_PIN = os.environ.get("ELMAX_PANEL_PIN")
LOCAL_TEST = os.environ.get("LOCAL_TEST", "false")
LOCAL_API_URL = os.environ.get("LOCAL_API_URL")

LOCAL_TEST = LOCAL_TEST.lower() == "true"

ONLINE_PANEL_ID = os.environ.get("ONLINE_PANEL_ID")