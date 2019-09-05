# /**********************************************************************
# *                                                                     *
# * Copyright (c) 2019 Hakan Seven <hakanseven12@gmail.com>             *
# *                                                                     *
# * This program is free software; you can redistribute it and/or modify*
# * it under the terms of the GNU Lesser General Public License (LGPL)  *
# * as published by the Free Software Foundation; either version 2 of   *
# * the License, or (at your option) any later version.                 *
# * for detail see the LICENCE text file.                               *
# *                                                                     *
# * This program is distributed in the hope that it will be useful,     *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of      *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
# * GNU Library General Public License for more details.                *
# *                                                                     *
# * You should have received a copy of the GNU Library General Public   *
# * License along with this program; if not, write to the Free Software *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
# * USA                                                                 *
# *                                                                     *
# ***********************************************************************

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Draft
import os


class CreateGuideLines:
    # Command to create guide lines for selected alignment.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap': Path + '/../Resources/Icons/CreateSections.svg',
        'MenuText': "Create Guide Lines",
        'ToolTip': "Create guide lines for selected alignment."
    }

    def __init__(self):
        # Import *.ui file(s)
        self.Path = os.path.dirname(os.path.abspath(__file__))

        self.IPFui = FreeCADGui.PySideUic.loadUi(
            self.Path + "/CreateGuideLines.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(
            self.Path + "/CreateGuideLinesGroup.ui")

        # To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateGuideLines)

        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.IPFui.AddGLGroupB.clicked.connect(self.load_cgl_gui)
        self.CPGui.OkB.clicked.connect(self.create_new_group)
        self.CPGui.CancelB.clicked.connect(self.CPGui.close)
        self.IPFui.AlignmentCB.currentIndexChanged.connect(
            self.ListGuideLinesGroups)
        self.IPFui.FromAlgStartChB.stateChanged.connect(self.ActivateStations)
        self.IPFui.ToAlgEndChB.stateChanged.connect(self.ActivateStations)

    def GetResources(self):
        # Return the command resources dictionary
        return self.Resources

    def activated(self):
        try:
            self.GuideLineGroup = FreeCAD.ActiveDocument.Guide_Lines
        except:
            self.GuideLineGroup = FreeCAD.ActiveDocument.addObject(
                "App::DocumentObjectGroup", 'Guide_Lines')
            self.GuideLineGroup.Label = "Guide Lines"
            FreeCAD.ActiveDocument.Alignments.addObject(self.GuideLineGroup)

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

        # List Alignments.
        self.IPFui.AlignmentCB.clear()
        alignment_group = FreeCAD.ActiveDocument.Alignments.Group
        self.alignment_list = []

        for Object in alignment_group:
            if Object.TypeId == 'Part::Part2DObjectPython':
                self.alignment_list.append(Object.Name)
                self.IPFui.AlignmentCB.addItem(Object.Label)

        self.list_guide_lines_groups()

    def get_alignment_info(self):
        alignment_index = self.IPFui.AlignmentCB.currentIndex()
        alignment_name = self.alignment_list[alignment_index]

        Alignment = FreeCAD.ActiveDocument.getObject(alignment_name)
        Start = Alignment.Proxy.model.data['meta']['StartStation']
        Length = Alignment.Proxy.model.data['meta']['Length']
        End = Start + Length/1000

        return Alignment, Start, End


    def ListGuideLinesGroups(self):

        # List Guide Lines Groups.
        self.IPFui.GLGroupCB.clear()
        guide_lines_group = FreeCAD.ActiveDocument.Guide_Lines.Group
        self.GLGList = []

        for Object in guide_lines_group:
            if Object.TypeId == 'App::DocumentObjectGroup':
                self.GLGList.append(Object.Name)
                self.IPFui.GLGroupCB.addItem(Object.Label)

        Alignment, Start, End = self.getAlignmentInfos()

        self.IPFui.StartStationLE.setText(str(round(Start, 3)))
        self.IPFui.EndStationLE.setText(str(round(End, 3)))

    def LoadCGLGui(self):

        # Load Create Guide Lines Group UI.
        self.CPGui.setParent(self.IPFui)
        self.CPGui.setWindowFlags(QtCore.Qt.Window)
        self.CPGui.show()


    def CreateNewGroup(self):
        # Create new guide lines group.
        NewGroupName = self.CPGui.GuideLinesGroupNameLE.text()
        NewGroup = FreeCAD.ActiveDocument.addObject(
            "App::DocumentObjectGroup", NewGroupName)
        NewGroup.Label = NewGroupName
        FreeCAD.ActiveDocument.Guide_Lines.addObject(NewGroup)
        self.IPFui.GLGroupCB.addItem(NewGroupName)
        self.GLGList.append(NewGroup.Name)
        NewGroup.Label = NewGroupName
        self.CPGui.close()

    def ActivateStations(self):
        # When QCheckBox status changed do the following options.
        Alignment, Start, End = self.getAlignmentInfos()
        if self.IPFui.FromAlgStartChB.isChecked():
            self.IPFui.StartStationLE.setEnabled(False)
            self.IPFui.StartStationLE.setText(str(round(Start, 3)))
        else:
            self.IPFui.StartStationLE.setEnabled(True)

        if self.IPFui.ToAlgEndChB.isChecked():
            self.IPFui.EndStationLE.setEnabled(False)
            self.IPFui.EndStationLE.setText(str(round(end, 3)))
        else:
            self.IPFui.EndStationLE.setEnabled(True)

    def create_guide_lines(self):
        l = self.IPFui.LeftLengthLE.text()
        r = self.IPFui.RightLengthLE.text()
        first_station = self.IPFui.StartStationLE.text()
        last_station = self.IPFui.EndStationLE.text()
        glg_index = self.IPFui.GLGroupCB.currentIndex()
        glg_index_name = self.GLGList[glg_index]
        tangent_increment = self.IPFui.TIncrementLE.text()
        curve_spiral_increment = self.IPFui.CSIncrementLE.text()

        alignment, start, end = self.get_alignment_info()
        pl = alignment.Placement.Base

        stations = []
        geometry = alignment.Proxy.model.data['geometry']
        for Geo in geometry:
            start_station = Geo.get('StartStation')
            end_station = Geo.get('StartStation')+Geo.get('Length')/1000
            if start_station != 0:
                if self.IPFui.HorGeoPointsChB.isChecked():
                    stations.append(start_station)

            if Geo.get('Type') == 'Line':
                for i in range(round(float(start_station)), round(float(end_station))):
                    if i % int(tangent_increment) == 0:
                        stations.append(i)

            elif Geo.get('Type') == 'Curve' or Geo["Type"] == 'Spiral':
                for i in range(round(float(StartStation)), round(float(EndStation))):
                    if i % int(CurveSpiralIncrement) == 0:
                        Stations.append(i)
        Stations.append(round(End, 3))

        Result = []
        for Station in Stations:
            if float(FirstStation) <= Station <= float(LastStation):
                Result.append(Station)
        Result.sort()

        for Station in Result:
            Coord, vec = Alignment.Proxy.model.get_orthogonal(Station, "Left")
            LeftEnd = Coord.add(FreeCAD.Vector(vec).multiply(int(L)*1000))
            RightEnd = Coord.add(vec.negative().multiply(int(R)*1000))

            GuideLine = Draft.makeWire([LeftEnd, Coord, RightEnd])
            GuideLine.Placement.move(Pl)
            GuideLine.Label = str(round(Station, 3))
            FreeCAD.ActiveDocument.getObject(GLGIndexName).addObject(GuideLine)
            FreeCAD.ActiveDocument.recompute()


FreeCADGui.addCommand('Create Guide Lines', CreateGuideLines())

