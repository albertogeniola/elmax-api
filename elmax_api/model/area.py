from typing import Dict


class Area():
    """Representation of an Area configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 status: str,
                 armed_status: str):
        self._endpoint_id = endpoint_id
        self._visible = visible
        self._index = index
        self._name = name
        self._status = status
        self._armed_status = armed_status

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
    def status(self) -> str:
        return self._status

    @property
    def armed_status(self) -> str:
        return self._armed_status

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Area':
        """Create a new area configuration object from the API json response"""
        area = Area(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            status=response_entry.get('stato'),
            armed_status=response_entry.get('statoInserimento')
        )
        return area
