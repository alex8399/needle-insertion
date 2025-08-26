import Sofa
import time

from needleMechanicalObjectController import NeedleMechanicalObjectController
from positionTracker import PositionTracker
from positionTransformer import NeedlePositionTransformer


class NeedleAnimationController(Sofa.Core.Controller):
    t: float

    mechanicalObjectController: NeedleMechanicalObjectController
    positionTracker: PositionTracker
    positionTransformer: NeedlePositionTransformer

    def __init__(self, needle: Sofa.Core.Node, **kwargs):
        super().__init__(**kwargs)
        self.t = 0.0

        self.mechanicalObjectController = NeedleMechanicalObjectController(
            needle)
        self.positionTracker = PositionTracker()
        self.positionTransformer = NeedlePositionTransformer()

        initialPosition = self.positionTransformer.getDefaultPosition()
        self.mechanicalObjectController.setPosition(initialPosition)

    def onAnimateBeginEvent(self, event) -> None:
        self.t += event["dt"]

        trackingPosition = self.positionTracker.getPosition()
        sofaPosition = self.positionTransformer.transformTrackerToSofaPosition(
            trackingPosition)
        self.mechanicalObjectController.setPosition(sofaPosition)