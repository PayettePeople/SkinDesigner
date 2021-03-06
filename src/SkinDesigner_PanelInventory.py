# SkinDesigner: A Plugin for Building Skin Design (GPL) started by Santiago Garay

# This file is part of SkinDesigner.
# 
# Copyright (c) 2017, Santiago Garay <sgaray1970@gmail.com> 
# SkinDesigner is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# SkinDesigner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SkinDesigner; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Use this component to display all panel types generated to develop the skin solution with a count of haw many panels are panel
On bold are displayed the panels types that have standard dimensiosn (not custom sized).

    Args:
        _skinPanelData:  A list with information on panel types generated by the SkinGenerator component.  
        showCustom: A boolean that specifies if includes or excludes the custom sized panels.
        drawGeometry: A boolean that turns on/off drawing of panel types in the scene.
        drawBreps: A boolean that turns on/off outputing grasshopper geometry versions of the panel types.
        panelIndex: An integer that specifies which panel index in the list of panels generated to display. By default it shows all the panels in the list.
        locPoint A grasshoper Point object to indicate the start point location in the scene to draw  the panel types.
        
    Returns:
        Breps: A list of Breps of the panels created when drawBreps is turned on.
"""

ghenv.Component.Name = "SkinDesigner_PanelInventory"
ghenv.Component.NickName = 'PanelInventory'
ghenv.Component.Message = 'VER 0.1.16\nSep_22_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "04 | Display"



import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
from types import *
SGLibPanel = sc.sticky["SGLib_Panel"]


PANEL_TYPES_ID=str(ghenv.Component.InstanceGuid)
warningData = []

def DeleteMockup():
    
    if not sc.sticky["PanelTypes_Data"+ PANEL_TYPES_ID] : return
        
    for data in sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] :
        if isinstance(data, SGLibPanel): data.HideAll() #same as deleting all panel objects
        elif rs.IsText(data) : rs.DeleteObject(data)
    

#initialize
sc.doc = rc.RhinoDoc.ActiveDoc
rs.EnableRedraw(False)

if _skinPanelData == []: warningData.append( "'_skinPanelData' input data missing")

locP = None
if  type(_locPoint) == rc.Geometry.ArcCurve: 
    success, circle = _locPoint.TryGetCircle()
    locP = circle.Center
elif type(_locPoint) == rc.Geometry.Point3d : locP = _locPoint
else: warningData.append( "I need a circle or point for location")

if locP: offsetX, offsetY, offsetZ = locP

if showCustom == None: showCustom = True
Mockup_Bay = [] ; textTypes = [] 
Breps = []

if "PanelTypes_Data"+PANEL_TYPES_ID not in sc.sticky : sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = []

DeleteMockup()

if _skinPanelData <> [] and locP:
    try:
        panelCounter = 0
        for panelData in _skinPanelData :
            for i in range(len(panelData)):
                panelCounter +=1
                if panelIndex <> None and panelCounter <> panelIndex: continue
                panelName = panelData[i][0].GetName()
                #print panelName
                if panelName.find("-Width")>0 or panelName.find("-Height")>0 or panelName.find(" Left")>0 or panelName.find(" Right")>0: 
                    if showCustom :fontHeight = 0.5 ; fontStyle=0 
                    else: continue #skip custom panel if showCustom off 
                else: fontHeight= .6 ; fontStyle = 1
                
                arrBoxPoints = [[offsetX, offsetY, offsetZ],[offsetX + panelData[i][0].GetPanelProperty("PanelWidth"), offsetY, offsetZ],\
                    [offsetX, offsetY, offsetZ+panelData[i][0].GetPanelProperty("PanelHeight")],\
                    [offsetX + panelData[i][0].GetPanelProperty("PanelWidth"), offsetY, offsetZ+panelData[i][0].GetPanelProperty("PanelHeight")]]
                    
                #create text info
                if drawGeometry:
                    blockCount = len(panelData[i][0].GetPanelProperty("BlockInstances"))
                    textTypes.append(rs.AddText(panelName + "   Count: " + str(blockCount), rs.PointSubtract(arrBoxPoints[0], [0,1,0]), fontHeight, font_style=fontStyle))
                    rs.RotateObject(textTypes[len(textTypes)-1], rs.TextObjectPoint(textTypes[len(textTypes)-1]), 270)
                
                #create panel copy
                Mockup_Bay.append(SGLibPanel())
                Mockup_Bay[len(Mockup_Bay)-1].Copy(panelData[i][0])
                Mockup_Bay[len(Mockup_Bay)-1].MorphPanel(arrBoxPoints)
                #print i; print panelData
                
                Mockup_Bay[len(Mockup_Bay)-1].Draw(drawGeometry)
                if  drawBreps : Breps += Mockup_Bay[len(Mockup_Bay)-1].GetBreps()
                offsetX = offsetX + Mockup_Bay[len(Mockup_Bay)-1].GetPanelProperty("PanelWidth")+ 1
    except:
        warningData.append( "Can not generate panel, check inputs")
        DeleteMockup()
    sc.sticky["PanelTypes_Data"+PANEL_TYPES_ID] = Mockup_Bay + textTypes
else:
    DeleteMockup()
    
#Wrapup
rs.EnableRedraw(True)
sc.doc = ghdoc

if warningData <> []: 
    for warning in warningData: ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, str(warning))

print "Done"