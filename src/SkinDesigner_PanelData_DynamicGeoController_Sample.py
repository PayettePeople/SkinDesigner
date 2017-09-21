


# By Santiago Garay
# Skin Generator

"""
Use this component python format to generate your own DynamicGeoemtry controller. 
This example is to be sued with the Fin DynamicGeoemtry provided. 
For more infomation refer to the Dynamic geometry grasshoper example file.

    Returns:
        dataFuntonP: A data function object to be connected to the PanelFunction component

"""

ghenv.Component.Name = "SkinDesigner_PanelData_DynamicGeoController_Sample"
ghenv.Component.NickName = 'PanelData_DynamicGeoControllerSample'
ghenv.Component.Message = 'VER 0.0.01\nSep_21_2017'
ghenv.Component.Category = "SkinDesigner"
ghenv.Component.SubCategory = "03 | Functions"
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

import rhinoscriptsyntax as rs
#import Rhino
#import scriptcontext as sc
from types import *
import random
import copy
#import math
#import imp



class PanelDataFunction:
    

    
    #CONSTRUCTOR -------------------------------------------------------------------------------------------
    def __init__(self):
        pass

    def Reset(self):
        pass

    
    def Run(self, dataInstance=None, valueMin=None, valueMax=None, numSamples=None, skinInstance=None, panelFlags=None):
        
        paramData = [[0,0],[1,0],[2,0],[3,0]]
        params = [0,1,2,3]
        generator = ([dataInstance, param] for param in params)
        newDataInstance = list(generator)
        #newDataInstance[0] = [0,0]
         
        cRow = skinInstance.GetProperty("SKIN_CURRENT_CELL_ROW")  
        cCol = skinInstance.GetProperty("SKIN_CURRENT_CELL_COLUMN") 
        bayPanelIndex = skinInstance.GetProperty("SKIN_CURRENT_BAY_PANEL_INDEX")
        panelPts = skinInstance.GetCellProperty(cRow, cCol, "PANEL_CORNER_POINTS", bayPanelIndex)
        
        chFlag = None; dynamicGeoParams = None
        bRow = cRow - 1 if cRow > 0 else None
        if bRow <> None :
            for index in range(skinInstance.GetCellProperty(bRow, cCol,"BAY_NUM_PANELS")): 
                cellPts = skinInstance.GetCellProperty(bRow, cCol, "PANEL_CORNER_POINTS",index)
                if panelPts[0] == cellPts[2] and panelPts[1] == cellPts[3] :
                    chFlag = skinInstance.GetCellProperty(bRow, cCol, "PANEL_CHANGE_FLAG", index)
                    break
            try:
                for customGeoFlag in chFlag[2]['CustomGeometry']:
                    #print ["Here", customGeoFlag]
                    if 'dynamicGeoParams' in customGeoFlag: 
                        codeObj= compile(customGeoFlag,'<string>','single') ; eval(codeObj) 
                        
            except: pass
        if dynamicGeoParams :
            newDataInstance[0][0] = dynamicGeoParams[3][0]
            
        return newDataInstance
        
        

            
        



dataFunctionP = PanelDataFunction()

print "Done"
