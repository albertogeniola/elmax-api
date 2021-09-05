class DeviceRegistry(object):
    """Representation of the devices registry."""

    def __init__(self):
        """Initialize the device registry."""
        self.devices_by_hash = {}

    def register(self, device):
        """Register a new device."""
        self.devices_by_hash[device.hash] = device

    def devices(self) -> list:
        """Get all available devices."""
        return list(self.devices_by_hash.values())
