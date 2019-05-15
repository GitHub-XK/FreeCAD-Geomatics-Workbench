import FreeCAD, FreeCADGui
import os
import Draft

class CreateContour:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Create Contour",
        'ToolTip' : "Create contour on selected surface."
    }

    def __init__(self):
        print ("Add Triangle Added")

    def GetResources(self):
        #Return the command resources dictionary
        return self.resources

    def Activated(self):
        Surface = FreeCADGui.Selection.getSelection()[-1]
        Base = Surface.Mesh.Placement.Base
        CopyMesh = Surface.Mesh.copy()
        try:
            self.Contours = FreeCAD.ActiveDocument.Contours
        except:
            self.Contours = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Contours')

        self.CreateContour(CopyMesh,Base)

    def CreateContour(self,Mesh,Base):
        zmax = Mesh.BoundBox.ZMax
        zmin = Mesh.BoundBox.ZMin
        DeltaH =1000

        for H in range(round(zmin), round(zmax)):
            if H % int(DeltaH) == 0:
                CrossSections = Mesh.crossSections([((0,0,H),(0,0,1))],0.000001)
                for i in CrossSections[0]:
                    Contour = Draft.makeWire(i)
                    Contour.Placement.Base = Contour.Placement.Base.add(Base)
                    self.Contours.addObject(Contour)

FreeCADGui.addCommand('Create Contour',CreateContour())
