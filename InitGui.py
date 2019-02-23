#***************************************************************************
#*   (c) Hakan Seven (hakanseven12@gmail.com) 2019                         *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *                                                  *
#***************************************************************************/



class GeomaticWorkbench ( Workbench ):
    "Geomatic workbench object"
    def __init__(self):
        #self.__class__.Icon = FreeCAD.getHomePath() + "Mod/Geomatic/Resources/icons/GeomaticWorkbench.svg"
        self.__class__.MenuText = "Geomatic"
        self.__class__.ToolTip = "Geomatic"

    def Initialize(self): #This function is executed when FreeCAD starts
        import ImportPointFile

        #Create Toolbar
        list = ['Import Point File']
        self.appendToolbar("Point Tools",list)

        #Create Point Groups
        FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Points')
        SubGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'All Points')
        FreeCAD.ActiveDocument.Points.addObject(SubGroup)

        #Create Menu
        #menu = ["Test &Commands","TestToolsGui"]
        #list = ["Std_TestQM","Std_TestReloadQM","Test_Test","Test_TestAll","Test_TestDoc","Test_TestBase"]
        #self.appendCommandbar("TestToolsGui",list)
        #self.appendMenu(menu,list)

    def Activated(self):
        #This function is executed when the workbench is activated

        return

Gui.addWorkbench(GeomaticWorkbench())

