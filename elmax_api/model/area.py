from typing import Dict

from elmax_api.model.alarm_status import AlarmStatus, AlarmArmStatus
from elmax_api.model.endpoint import DeviceEndpoint


class Area(DeviceEndpoint):
    """Representation of an Area configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 status: AlarmStatus,
                 armed_status: AlarmArmStatus):
        super().__init__(endpoint_id=endpoint_id, visible=visible, index=index, name=name)
        self._status = status
        self._armed_status = armed_status

    @property
    def alarm_status(self) -> AlarmStatus:
        """
        Current alarm status.

        Returns: `AlarmStatus`

        """
        return self._status

    @property
    def armed_status(self) -> AlarmArmStatus:
        """
        Current alarm arm status

        Returns: `AlarmArmStatus`

        """
        return self._armed_status

    def __eq__(self, other):
        super_equals = super().__eq__(other)
        if not super_equals:
            return False
        return self.alarm_status == other.alarm_status and self.armed_status==other.armed_status

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Area':
        """Create a new area configuration object from the API json response"""
        area = Area(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            status=AlarmStatus(response_entry['statoInserimento']),
            armed_status=AlarmArmStatus(response_entry['stato'])
        )
        return area
