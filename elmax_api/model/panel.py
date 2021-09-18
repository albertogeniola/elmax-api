from typing import Dict, List, Any

from elmax_api.model.actuator import Actuator
from elmax_api.model.area import Area
from elmax_api.model.goup import Group
from elmax_api.model.scene import Scene
from elmax_api.model.zone import Zone


class PanelEntry:
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
    def from_api_response(response_entry: Dict) -> 'PanelEntry':
        """Create a new control panel from the API json response"""
        # Convert the data structure so that we have a dictionary of names by user
        name_by_user = dict()
        for entry in response_entry.get("username", []):
            username = entry.get("name")
            name = entry.get("label")
            name_by_user[username] = name

        control_panel = PanelEntry(
            devicehash=response_entry["hash"],
            online=bool(response_entry["centrale_online"]),
            name_by_user=name_by_user,
        )
        return control_panel


class PanelStatus:
    """Representation of a panel status"""

    def __init__(self,
                 panel_id: str,
                 user_email: str,
                 release: str,
                 cover_feature: bool,
                 scene_feature: bool,
                 zones: List[Zone],
                 actuators: List[Actuator],
                 areas: List[Area],
                 groups: List[Group],
                 scenes: List[Scene],
                 # TODO: Implement covers
                 covers: List[Any]):

        self._panel_id = panel_id
        self._user_email = user_email
        self._release = release
        self._cover_feature = cover_feature
        self._scene_feature = scene_feature
        self._zones = zones
        self._actuators = actuators
        self._areas = areas
        self._groups = groups
        self._scenes = scenes
        self._covers = covers

    @property
    def panel_id(self) -> str:
        return self._panel_id

    @property
    def user_email(self) -> str:
        return self._user_email

    @property
    def release(self) -> str:
        return self._release

    @property
    def cover_feature(self) -> bool:
        return self._cover_feature

    @property
    def scene_feature(self) -> bool:
        return self._scene_feature

    @property
    def zones(self) -> List[Zone]:
        return self._zones

    @property
    def actuators(self) -> List[Actuator]:
        return self._actuators

    @property
    def areas(self) -> List[Area]:
        return self._areas

    @property
    def groups(self) -> List[Group]:
        return self._groups

    @property
    def scenes(self) -> List[Scene]:
        return self._scenes

    @property
    def covers(self) -> List[Any]:  # TODO: Update type once defined
        return self._covers

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'PanelStatus':
        """Create a new panel status object from the API json response"""
        panel_status = PanelStatus(
            panel_id=response_entry.get('centrale'),
            user_email=response_entry.get('utente'),
            release=response_entry.get('release'),
            cover_feature=response_entry.get('tappFeature'),
            scene_feature=response_entry.get('sceneFeature'),
            zones=response_entry.get('zone'),
            actuators=response_entry.get('uscite'),
            areas=response_entry.get('aree'),
            covers=response_entry.get('tapparelle'),
            groups=response_entry.get('groups'),
            scenes=response_entry.get('scenari')
        )
        return panel_status