import Sofa

from structs import SofaColor


class HandColorController:
    body: Sofa.Core.Node

    def __init__(self, hand: Sofa.Core.Node):
        self.body = hand

    def setColor(self, color: SofaColor) -> None:
        rgba = color.color
        rgbaStr = tuple("{:.3}".format(i) for i in rgba)
        diffuse = f"Diffuse 1 {rgbaStr[0]} {rgbaStr[1]} {rgbaStr[2]} {rgbaStr[3]}"
        self.body.visual.visual.material.value = f"Default {diffuse}"