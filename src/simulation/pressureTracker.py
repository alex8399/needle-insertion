from structs import TrackingPressure
from port import AbstractPortControllerSingleton, Bar9600COM3PortControllerSingleton


class PressureTracker:
    portController: AbstractPortControllerSingleton

    def __init__(self):
        self.portController = Bar9600COM3PortControllerSingleton()

    def getPressure(self) -> TrackingPressure:
        portData = self.portController.getData()
        force = portData["force"]
        pressure = TrackingPressure(force=force)
        return pressure