import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import os

class ExportPoints:
    #Command to export points to point file.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap'  : Path + '/../Resources/Icons/ExportPoints.svg',
        'MenuText': "Export Points",
        'ToolTip' : "Export points to point file."
    }

    def __init__(self):
        #Import *.ui file.
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/ExportPoints.ui")

        #To Do List.
        self.IPFui.BrowseB.clicked.connect(self.FileDestination)
        self.IPFui.ExportB.clicked.connect(self.ExportPointsToFile)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def GetResources(self):
        #Return the command resources dictionary
        return self.Resources

    def Activated(self):
        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

        self.IPFui.FileDestinationLE.clear()
        self.IPFui.PointGroupsLW.clear()
        SG = FreeCAD.ActiveDocument.Point_Groups.Group
        OutList = FreeCAD.ActiveDocument.Point_Groups.OutList
        self.GroupList = []
        Count = 0

        for i in OutList:
            self.GroupList.append(SG[Count].Name)
            SubGroupName = SG[Count].Label
            self.IPFui.PointGroupsLW.addItem(SubGroupName)
            Count = Count + 1

    def FileDestination(self):
        #Get file destination.
        fileName = QtGui.QFileDialog.getSaveFileName(None, 'Save File', os.getenv("HOME"), Filter='*.txt')
        self.IPFui.FileDestinationLE.setText(fileName[0]+".txt")

    def ExportPointsToFile(self):
        #Import UI variables.
        PointName = self.IPFui.PointNameLE.text()
        Northing = self.IPFui.NorthingLE.text()
        Easting = self.IPFui.EastingLE.text()
        Elevation = self.IPFui.ElevationLE.text()
        Description = self.IPFui.DescriptionLE.text()
        Format = ["","","","",""]
        FileDestinationLE = self.IPFui.FileDestinationLE.text()
        if self.IPFui.DelimiterCB.currentText() == "Space":
            Delimiter = ' '
        elif self.IPFui.DelimiterCB.currentText() == "Comma":
            Delimiter=','
        GroupCounter = 0

        #Create point file.
        File = open(FileDestinationLE, 'w')
        for i in self.IPFui.PointGroupsLW.selectedIndexes():
            Selections = self.IPFui.PointGroupsLW.selectedIndexes()[GroupCounter]
            Index = int(Selections.row())
            SPG = self.GroupList[Index]
            GroupName = FreeCAD.ActiveDocument.getObject(SPG).Group
            OutList = FreeCAD.ActiveDocument.getObject(SPG).OutList
            limits = range(1,int(len(OutList)+1))
            GroupCounter = GroupCounter + 1
            Count = 0

            for i in limits:
                pn = str(GroupName[Count].Label)
                xx = str(round(float(GroupName[Count].X))/1000)
                yy = str(round(float(GroupName[Count].Y))/1000)
                zz = str(round(float(GroupName[Count].Z))/1000)
                Format[int(PointName)-1] = pn
                Format[int(Easting)-1] = xx
                Format[int(Northing)-1] = yy
                Format[int(Elevation)-1] = zz
                Format[int(Description)-1] = ""

                File.write(Format[0]+Delimiter+Format[1]+Delimiter+Format[2]+Delimiter+Format[3]+Delimiter+Format[4]+"\n")
                Count = Count + 1
        File.close()

FreeCADGui.addCommand('Export Points',ExportPoints()) 
