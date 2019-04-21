import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import os
import numpy as np
import scipy.spatial
from scipy.spatial import Delaunay
import Mesh

class CreateSurface:
    """
    Command to create a new surface
    """

    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/Resources/Icons/CreateSurface.svg',
        'MenuText': "Create Surface",
        'ToolTip' : "Create surface from selected point group(s)."
    }

    def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/Resources/UI/CreateSurface.ui")
        self.IPFui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateSurface)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return self.resources

    def Activated(self):
        self.IPFui.show()
        model = QtGui.QStandardItemModel()
        self.IPFui.PointGroupsLV.setModel(model)

        SG = FreeCAD.ActiveDocument.Point_Groups.Group
        OutList = FreeCAD.ActiveDocument.Point_Groups.OutList
        self.GroupList = []
        Count = 0

        for i in OutList:
            self.GroupList.append(SG[Count].Name)
            SubGroupName = SG[Count].Label
            item = QtGui.QStandardItem(SubGroupName)
            model.appendRow(item)
            Count = Count + 1

    def CreateSurface(self):
        #Import UI variables
        SurfaceNameLE = self.IPFui.SurfaceNameLE.text()
        trp = []
        GroupCounter = 0

        #Create surface
        for i in self.IPFui.PointGroupsLV.selectedIndexes():
            Selections = self.IPFui.PointGroupsLV.selectedIndexes()[GroupCounter]
            Index = int(Selections.row())
            SPG = self.GroupList[Index]
            GroupName = FreeCAD.ActiveDocument.getObject(SPG).Group
            OutList = FreeCAD.ActiveDocument.getObject(SPG).OutList
            limits = range(1,int(len(OutList)+1))
            GroupCounter = GroupCounter + 1
            Count = 0

            for i in limits:
                xx = float(GroupName[Count].X)
                yy = float(GroupName[Count].Y)
                zz = float(GroupName[Count].Z)
                trp.append([xx,yy,zz])
                Count = Count + 1

        data = np.array(trp)
        test = np.array(trp)
        test -= test.mean(axis=0)
        tri = scipy.spatial.Delaunay( test[:,:2]) 

        plotMesh = []

        for i in tri.vertices:

           first = int(i[0])
           second = int(i[1])
           third = int(i[2])

           plotMesh.append(data[first])
           plotMesh.append(data[second])
           plotMesh.append(data[third])

        plotMeshObject = Mesh.Mesh(plotMesh)
        Surface = FreeCAD.ActiveDocument.addObject("Mesh::Feature", SurfaceNameLE)
        Surface.Mesh = plotMeshObject
        FreeCAD.ActiveDocument.Surfaces.addObject(Surface)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 
