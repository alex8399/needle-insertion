import Sofa

from structs import TrackingPosition, SofaPosition
from pressureTracker import PressureTracker
from handColorController import HandColorController
from pressureToColorTransformer import PressureToColorTransformer


class HandAnimationController(Sofa.Core.Controller):
    t: float
    
    colorController: HandColorController
    pressureTracker: PressureTracker
    pressureToColorTransformer: PressureToColorTransformer

    def __init__(self, hand: Sofa.Core.Node, **kwargs):
        super().__init__(**kwargs)
        self.t = 0.0

        self.colorController = HandColorController(hand)
        self.pressureTracker = PressureTracker()
        self.pressureToColorTransformer = PressureToColorTransformer()
        
        initialColor = self.pressureToColorTransformer.getColorFromGradient(0)
        self.colorController.setColor(initialColor)

    def onAnimateBeginEvent(self, event) -> None:
        self.t += event["dt"]
        
        pressure = self.pressureTracker.getPressure()
        color = self.pressureToColorTransformer.transformPressureToColor(pressure)
        self.colorController.setColor(color)