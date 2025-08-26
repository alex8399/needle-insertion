from structs import TrackingPosition, Rotation, Distance
from port import AbstractPortControllerSingleton, Bar9600COM3PortControllerSingleton


class PositionTracker:
    portController: AbstractPortControllerSingleton

    def __init__(self):
        self.portController = Bar9600COM3PortControllerSingleton()

    def getPosition(self) -> TrackingPosition:
        portData = self.portController.getData()

        roll = portData["roll"]
        pitch = portData["pitch"]
        yaw = portData["yaw"]
        range = portData["range"]

        position = TrackingPosition(
            Rotation(roll=roll, pitch=pitch, yaw=yaw),
            Distance(range=range))
        return position
