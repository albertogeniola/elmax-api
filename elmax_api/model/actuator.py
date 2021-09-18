from typing import Dict


class Actuator():
    """Representation of an actuator"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 opened: bool):
        self._endpoint_id = endpoint_id
        self._visible = visible
        self._index = index
        self._name = name
        self._opened = opened

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

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Actuator':
        """Create a new actuator object from the API json response"""
        actuator = Actuator(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            opened=response_entry.get('aperta')
        )
        return actuator
