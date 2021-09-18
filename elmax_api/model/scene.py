from typing import Dict


class Scene():
    """Representation of a Scene configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str):
        self._endpoint_id = endpoint_id
        self._visible = visible
        self._index = index
        self._name = name

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

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Scene':
        """Create a new scene configuration object from the API json response"""
        scene = Scene(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
        )
        return scene
