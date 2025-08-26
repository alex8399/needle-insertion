import Sofa
import Sofa.Gui

import numpy as np

from needleAnimationController import NeedleAnimationController
from handAnimationController import HandAnimationController


class SofaScene:
    WINDOW_WIDTH: int = 1500
    WINDOW_HEIGHT: int = 1500

    root: Sofa.Core.Node

    def __init__(self):
        root = Sofa.Core.Node("root")
        self.root = root

    def exec(self) -> None:
        self.createScene()
        Sofa.Simulation.initRoot(self.root)
        Sofa.Gui.GUIManager.Init("TissueScene", "qglviewer")
        Sofa.Gui.GUIManager.createGUI(self.root, __file__)
        Sofa.Gui.GUIManager.SetDimension(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        Sofa.Gui.GUIManager.MainLoop(self.root)
        Sofa.Gui.GUIManager.closeGUI()

    def addNeedle(self) -> None:
        needle = self.root.addChild("needle")

        needle.addObject("MechanicalObject", name="mstate", template="Rigid3d",
                         position=[[0, 15, 0, 0, 0, 0, 1]], showObject=True)
        needle.addObject("UniformMass", totalMass=100.0)

        visual = needle.addChild("VisualModel")
        visual.addObject("MeshOBJLoader", name="loader", filename="mesh/needle.obj")
        visual.addObject("OglModel", name="visual", src="@loader", scale3d=[0.02]*3, color=[1.0, 1.0, 1.0, 1.0])
        visual.addObject("RigidMapping")

    def addDeformableTissue(self, young=18000.0, poisson=0.48):
        tissue = self.root.addChild("skinTissue")

        loader = tissue.addObject("MeshGmshLoader", name="loader",
                                  filename="mesh/skin_layer.msh", createSubelements=True)
        loader.scale = 1.0

        tissue.addObject("TetrahedronSetTopologyContainer", name="topo", src="@loader")
        tissue.addObject("TetrahedronSetGeometryAlgorithms")
        tissue.addObject("TetrahedronSetTopologyModifier")
        tissue.addObject("MechanicalObject", name="mstate", scale3d=[2.]*3, position=[[0, 0, 0]], template="Vec3d")

        tissue.addObject("UniformMass", totalMass=0.02)
        tissue.addObject("TetrahedronFEMForceField", name="fem",
                         youngModulus=young, poissonRatio=poisson, method="large")
        tissue.addObject("EulerImplicitSolver", rayleighStiffness=0.005, rayleighMass=0.03)
        tissue.addObject("SparseLDLSolver", template="CompressedRowSparseMatrixMat3x3d")
        tissue.addObject("LinearSolverConstraintCorrection")

        tissue.addObject("BoxROI", name="roi", box=[-10, 0, -10, 10, 10, 10], drawBoxes=True)
        tissue.addObject("RestShapeSpringsForceField", points="@roi.indices", stiffness=1000)

        surf = tissue.addChild("Surface")
        surf.addObject("TriangleSetTopologyContainer", name="surface", src="@../topo")
        surf.addObject("TriangleSetTopologyModifier")
        surf.addObject("TriangleSetGeometryAlgorithms", template="Vec3d")
        surf.addObject("Tetra2TriangleTopologicalMapping", input="@../topo", output="@surface")
        surf.addObject("MechanicalObject", name="cstate", template="Vec3d", position="@../mstate.position")
        surf.addObject("TriangleCollisionModel")
        surf.addObject("PointCollisionModel")
        surf.addObject("LineCollisionModel")
        surf.addObject("BarycentricMapping", input="@../mstate", output="@cstate")

        visual = tissue.addChild("VisualModel", name="visual")
        visual.addObject("OglModel", name="visual", color=[0.8, 0.5, 0.5, 1.], scale3d=[1.]*3)
        visual.addObject("IdentityMapping", input="@../mstate", output="@visual")

    def createScene(self) -> Sofa.Core.Node:
        self.root.dt = 0.01

        for i, plugin in enumerate([
            "Sofa.Component.Visual",
            "Sofa.GL.Component.Rendering3D",
            "Sofa.Component.StateContainer",
            "Sofa.Component.IO.Mesh",
            "Sofa.Component.Mapping.NonLinear",
            "Sofa.Component.Topology.Container.Dynamic",
            "Sofa.Component.Mass",
            "Sofa.Component.SolidMechanics.FEM.Elastic",
            "Sofa.Component.ODESolver.Backward",
            "Sofa.Component.LinearSolver.Direct",
            "Sofa.Component.Constraint.Lagrangian.Correction",
            "Sofa.Component.Constraint.Lagrangian.Model",
            "Sofa.Component.Engine.Select",
            "Sofa.Component.Collision.Geometry",
            "Sofa.Component.Collision.Detection.Algorithm",
            "Sofa.Component.Collision.Detection.Intersection",
            "Sofa.Component.Mapping.Linear",
            "Sofa.Component.SolidMechanics.Spring",
            "Sofa.Component.SceneUtility",
            "Sofa.Component.Topology.Mapping",
            "Sofa.Component.Collision.Response.Contact",
            "Sofa.Component.Constraint.Lagrangian.Solver",
            "Sofa.Component.AnimationLoop",
            "Sofa.GL.Component.Shader",
            "Sofa.Component.Setting",
        ]):
            self.root.addObject("RequiredPlugin", name=f"RequiredPlugin_{i}", pluginName=plugin, printLog=False)
        
        self.root.addObject("LightManager")
        self.root.addObject("DirectionalLight", direction=[-0.3, -1.0, -0.5], color=[1.0, 1.0, 1.0])
        self.root.addObject("SpotLight", position=[0, 200, 100], direction=[0, -1, -1], cutoff=45)

        self.root.addObject("BackgroundSetting", color=[0.95, 0.95, 0.95])

        self.root.addObject("DefaultVisualManagerLoop")
        self.root.addObject("FreeMotionAnimationLoop")
        self.root.addObject("GenericConstraintSolver", maxIterations=1000, tolerance=1e-3)
        self.root.addObject("VisualStyle", displayFlags="showVisual")
        self.root.addObject("OglSceneFrame", style="Arrows", alignment="TopRight")

        self.addNeedle()
        self.addDeformableTissue()

        self.root.addObject(NeedleAnimationController(self.root.needle))
        self.root.addObject(HandAnimationController(self.root.skinTissue))

        return self.root
