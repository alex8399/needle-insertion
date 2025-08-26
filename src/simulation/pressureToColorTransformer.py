import numpy as np
from typing import Tuple

from structs import SofaColor, TrackingPressure


class PressureToColorTransformer:
    FORCE_MIN: float = 50.
    FORCE_MAX: float = 200.

    RGB_START_GRADIENT_COLOR: Tuple[float, float, float] = (255., 192., 128.)
    RGB_END_GRADIENT_COLOR: Tuple[float, float, float] = (255., 85., 0.)
    GRADIENT_COLOR_NUMBER: int = 50
    OPACITY: float = 1.

    colorGradient: Tuple[SofaColor]

    def __init__(self):
        self.colorGradient = self.getColorGradient(self.RGB_START_GRADIENT_COLOR,
                                                   self.RGB_END_GRADIENT_COLOR,
                                                   self.GRADIENT_COLOR_NUMBER,
                                                   self.OPACITY)

    @staticmethod
    def getColorGradient(rgbStartColor: Tuple[float, float, float],
                         rgbEndColor: Tuple[float, float, float],
                         gradientColorNumber: int,
                         opacity: float) -> Tuple[SofaColor]:

        start, end = np.array(rgbStartColor), np.array(rgbEndColor)
        t = np.linspace(0, 1, gradientColorNumber)[:, None]
        rgbGradient = (start + (end - start) * t).astype(int)

        rgba01Gradient = list()
        for rgbColor in rgbGradient:
            rgba01Gradient.append(
                SofaColor(color=(
                    float(rgbColor[0]) / 255.,
                    float(rgbColor[1]) / 255.,
                    float(rgbColor[2]) / 255.,
                    opacity)))

        return tuple(rgba01Gradient)

    def getColorFromGradient(self, colorCoeff: float) -> SofaColor:
        colorInd = int(colorCoeff * len(self.colorGradient))
        colorInd = max(0, colorInd)
        colorInd = min(len(self.colorGradient) - 1, colorInd)
        return self.colorGradient[colorInd]

    def transformPressureToColor(self, pressure: TrackingPressure) -> SofaColor:
        colorCoeff = (pressure.force - self.FORCE_MIN) / \
            (self.FORCE_MAX - self.FORCE_MIN)

        return self.getColorFromGradient(colorCoeff)
