from dataclasses import dataclass
from typing import Tuple


@dataclass
class Rotation:
    roll: float
    yaw: float
    pitch: float


@dataclass
class Distance:
    range: float


@dataclass
class Quaternion:
    x: float
    y: float
    z: float
    w: float


@dataclass
class Location:
    x: float
    y: float
    z: float


@dataclass
class TrackingPosition:
    rotation: Rotation
    distance: Distance


@dataclass
class SofaPosition:
    location: Location
    quat: Quaternion


@dataclass
class TrackingPressure:
    force: float


@dataclass
class SofaColor:
    color: Tuple[float, float, float, float]
