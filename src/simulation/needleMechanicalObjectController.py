import Sofa
import numpy as np

from structs import SofaPosition


class NeedleMechanicalObjectController:
    body: Sofa.Core.Node

    def __init__(self, node):
        self.body = node

    def setPosition(self, position: SofaPosition) -> None:
        npArrayPosition = np.array([[
            position.location.x,
            position.location.y,
            position.location.z,
            position.quat.x,
            position.quat.z,
            position.quat.y,
            position.quat.w
        ]], dtype=float)

        self.body.mstate.position.value = npArrayPosition
