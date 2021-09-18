from typing import Dict


class Zone():
    """Representation of a zone configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 opened: bool,
                 excluded: bool):
        self._endpoint_id = endpoint_id
        self._visible = visible
        self._index = index
        self._name = name
        self._opened = opened
        self._excluded = excluded

    @property
    def endpoint_id(self) -> str:
        return self._endpoint_id

    @property
    def visible(self) -> bool:
        return self._visible

    @property
    def index(self) -> int:
        return self._index

    @property
    def name(self) -> str:
        return self._name

    @property
    def opened(self) -> bool:
        return self._opened

    @property
    def excluded(self) -> bool:
        return self._excluded

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Zone':
        """Create a new zone configuration object from the API json response"""
        zone = Zone(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            opened=response_entry.get('aperta'),
            excluded=response_entry.get('esclusa')
        )
        return zone
