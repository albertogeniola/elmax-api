from typing import Dict


class ControlPanel:
    """Representation of an available control panel."""

    def __init__(self, devicehash: str, online: bool, name_by_user: Dict[str, str]):
        """Initialize the new control panel."""
        self._hash = devicehash
        self._online = online
        self._names = name_by_user

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def online(self) -> bool:
        return self._online

    def get_name_by_user(self, username: str) -> str:
        if username not in self._names:
            ValueError(
                "Cannot find the name associated by user %s to device %s",
                username,
                self._hash,
            )
        return self._names.get(username)

    @staticmethod
    def from_api_response(response_entry: Dict):
        """Create a new control panel from the API json response"""
        # Convert the data structure so that we have a dictionary of names by user
        name_by_user = dict()
        for entry in response_entry.get("username", []):
            username = entry.get("name")
            name = entry.get("label")
            name_by_user[username] = name

        control_panel = ControlPanel(
            devicehash=response_entry["hash"],
            online=bool(response_entry["centrale_online"]),
            name_by_user=name_by_user,
        )
        return control_panel
