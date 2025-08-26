from scipy.spatial.transform import Rotation as Rot
import math

from structs import TrackingPosition, SofaPosition, Location, Quaternion, Rotation


class NeedlePositionTransformer:

    RANGE_OFFSET: float = 4.
    Y_OFFSET: float = 1.3
    Y_CORRECTION_SCALE: float = 5.
    PITCH_CORRECTION_THRESHOLD: float = 35.

    MAX_SENSOR_RANGE: float = 255.
    REALITY_TO_SIMULATION_SCALE: float = 0.14

    DEFAULT_LOCATION: Location = Location(x=20., y=15., z=12.)
    DEFAULT_QUAT: Quaternion = Quaternion(x=0, y=0, z=0, w=1)

    def getDefaultPosition(self) -> SofaPosition:
        return SofaPosition(quat=self.DEFAULT_QUAT, location=self.DEFAULT_LOCATION)

    def transformTrackerToSofaPosition(self, trackingPosition: TrackingPosition) -> SofaPosition:
        yaw = trackingPosition.rotation.yaw
        pitch = trackingPosition.rotation.pitch
        roll = trackingPosition.rotation.roll
        range = trackingPosition.distance.range

        qx, qy, qz, qw = Rot.from_euler(
            "zyx", [yaw, pitch, roll], degrees=True).as_quat()

        x = self.DEFAULT_LOCATION.x
        y = self.DEFAULT_LOCATION.y
        z = self.DEFAULT_LOCATION.z

        if range < self.MAX_SENSOR_RANGE:
            y = self.Y_OFFSET + (range * self.REALITY_TO_SIMULATION_SCALE +
                                 self.RANGE_OFFSET) * math.sin(math.radians(pitch))

            if abs(pitch) < self.PITCH_CORRECTION_THRESHOLD:
                yCorrection = (self.PITCH_CORRECTION_THRESHOLD -
                               abs(pitch)) / self.PITCH_CORRECTION_THRESHOLD
                y += self.Y_CORRECTION_SCALE * yCorrection

        sofaPosition = SofaPosition(
            location=Location(x=x, y=y, z=z),
            quat=Quaternion(x=qx, y=qy, z=qz, w=qw))
        return sofaPosition
