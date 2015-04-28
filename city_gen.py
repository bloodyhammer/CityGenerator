import bpy
import math
import random
from random import randint
from random import uniform
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(bpy.data.filepath))

from tools_blender import *

import bmesh
import bpy
from random import *
from bpy.props import *
from math import *
 
#properties of the panel
def initSceneProperties(scn):
	bpy.types.Scene.Margin = IntProperty(
		name = "Margin", 
		description = "Enter an integer",
		default = 10,
		min = 5,
		max = 30)
	bpy.types.Scene.Taille = IntProperty(
		name = "Taille", 
		description = "Enter an integer",
		default = 170,
		min = 50,
		max = 200)
	bpy.types.Scene.ValueHouse = FloatProperty(
		name = "% House", 
		description = "Enter an float",
		default = 0.2,
		min = 0,
		max = 1)
	bpy.types.Scene.ValueLittle = FloatProperty(
		name = "% Little Building", 
		description = "Enter an float",
		default = 0.2,
		min = 0,
		max = 1)
	bpy.types.Scene.ValueBig = FloatProperty(
		name = "% Big Building", 
		description = "Enter an float",
		default = 0.2,
		min = 0,
		max = 1)
	return

initSceneProperties(bpy.context.scene)
#gui panel
class ToolsPanel(bpy.types.Panel):
	bl_label = "Tools For Town"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
 
	def draw(self, context):
		layout = self.layout
		scn = context.scene
		
		layout.label("Parameters")
		row = layout.row(align=True)
		row = layout.row()
		split = row.split(percentage=0.8)
		col = split.column()
		col.prop(scn, 'Taille', text = "taille")
		col.prop(scn, 'Margin', text = "margin")
		split = row.split(percentage=1)
		col = split.column()
		col.prop(scn, 'ValueHouse', text = "% house")
		col.prop(scn, 'ValueLittle', text = "% little building")
		col.prop(scn, 'ValueBig', text = "% big building")
		
		layout.label("Tools")
		row = layout.row()
		split = row.split(percentage=1)
		col = split.column()
		col.operator("town.gen")
		col.operator("town.delete")
		split = row.split(percentage=1)
		col = split.column()
		col.operator("town.export")
		
		
		layout.label("Debug")
		row = layout.row()
		split = row.split(percentage=1)
		col = split.column()
		col.operator("town.print_index")

class OBJECT_OT_GenButton(bpy.types.Operator):
	bl_idname = "town.gen"
	bl_label = "Create town"
	def execute(self, context):
		margin = bpy.context.scene.Margin
		taille = bpy.context.scene.Taille
		valueHouse = bpy.context.scene.ValueHouse
		valueLittle = bpy.context.scene.ValueLittle
		valueBig = bpy.context.scene.ValueBig
		generate_town(taille, margin, valueHouse, valueLittle, valueBig)
		return{'FINISHED'}    

class OBJECT_OT_DeleteButton(bpy.types.Operator):
	bl_idname = "town.delete"
	bl_label = "Delete town"
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			ob.select = (ob.type == 'MESH' or ob.type == 'LAMP') and (ob.name.startswith("Cylinder") or ob.name.startswith("Cube") or ob.name.startswith("Plane"))
			bpy.ops.object.delete()
		return{'FINISHED'}    

class OBJECT_OT_PrintButton(bpy.types.Operator):
	bl_idname = "town.print_index"
	bl_label = "Print Index"
	def execute(self, context):
		print_index()
		return{'FINISHED'}    
		
class OBJECT_OT_ExportButton(bpy.types.Operator):
	bl_idname = "town.export"
	bl_label = "Export to FBX"
	def execute(self, context):
		convertToFbx()
		return{'FINISHED'}    

#registration
bpy.utils.register_module(__name__)


def generate_town(taille, margeBetweenBat, valueHouse, valueLittle, valueBig):
	margin = 5
	
	#CREATE BUILDINGS
	#SET FLOOR
	bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
	bpy.ops.transform.resize(value=(taille, taille, 0)) 

	#BUILDINGS POSITIONS
	x=- (taille - margin)
	y=- (taille - margin)
	nbUnitPerCote = (((taille - margin) * 2) / margeBetweenBat) + 1;
	
	nbBat = nbUnitPerCote * nbUnitPerCote;
	buildingPosTab = np.zeros((nbBat, 2), dtype='i')
	
	i=0
	for posNumX in range(0, int(nbBat/nbUnitPerCote)):
		for posNumY in range(0,int(nbBat/nbUnitPerCote)): 
			print(posNumX)
			print(posNumY)                         
			buildingPosTab[i][0] = x
			buildingPosTab[i][1] = y
			i = i+1
			y = y+margeBetweenBat
		y = -(taille - margin)
		x = x+margeBetweenBat 
	print(buildingPosTab)

	i = 0
	
	rangeHouse = taille - taille * valueHouse
	rangeLittleBuilding = taille - taille * (valueHouse + valueLittle)
	rangeBigBuilding = taille - taille * (valueHouse + valueLittle + valueBig)

	for buildNum in range(0,len(buildingPosTab)):
		#randPositionX = uniform(-50,50) 
		#randPositionY = uniform(-50,50) 
		positionX = buildingPosTab[i][0]
		positionY = buildingPosTab[i][1]
		#Centralisation des populations
		randBatiment = randint(0, 3)
		if positionX >= -rangeBigBuilding and positionX <= rangeBigBuilding and positionY >= -rangeBigBuilding and positionY <= rangeBigBuilding:       
			#if randBatiment == 0:
			createTower(positionX, positionY) 
		elif (positionX >= -rangeLittleBuilding and positionX <= -rangeBigBuilding and positionY >= -rangeLittleBuilding and positionY <= rangeLittleBuilding) or (positionX >= rangeBigBuilding and positionX <= rangeLittleBuilding and positionY >= -rangeLittleBuilding and positionY <= rangeLittleBuilding) or (positionX >= -rangeLittleBuilding and positionX <= rangeLittleBuilding and positionY >= -rangeLittleBuilding and positionY <= -rangeBigBuilding) or (positionX >= -rangeLittleBuilding and positionX <= rangeLittleBuilding and positionY >= rangeBigBuilding and positionY <= rangeLittleBuilding) :
			#elif randBatiment == 1:
				createBigBuilding(positionX, positionY) 
		elif (positionX >= -rangeHouse and positionX <= -rangeLittleBuilding and positionY >= -rangeHouse and positionY <= rangeHouse) or (positionX >= rangeLittleBuilding and positionX <= rangeHouse and positionY >= -rangeHouse and positionY <= rangeHouse) or (positionX >= -rangeHouse and positionX <= rangeHouse and positionY >= -rangeHouse and positionY <= -rangeLittleBuilding) or (positionX >= -rangeHouse and positionX <= rangeHouse and positionY >= rangeLittleBuilding and positionY <= rangeHouse):
			#elif randBatiment == 2:
				createLittleBuilding(positionX, positionY)
		elif positionX <= -rangeHouse or positionX >= rangeHouse or positionY <= -rangeHouse or positionY >= rangeHouse:
		   # elif randBatiment == 3:
			createHouse(positionX, positionY)
		"""else:
			if randBatiment == 0:
				createLittleBuilding(positionX, positionY)
			else:
				createBigBuilding(positionX, positionY) """
		i = i+1



	"""
	bpy.ops.object.mode_set(mode = 'OBJECT') 
	bpy.ops.mesh.primitive_circle_add(enter_editmode = True, location = (0, 0, 13))
	bpy.ops.object.mode_set(mode = 'EDIT') 
	randomSize = randint(3, 5)
	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value" : (0,0,randomSize)})            
	randomCoorX = uniform(-4, 8)
	nodePosition[i][0] = (0 + randomCoorX)
	randomCoorY = uniform(-4, 8)
	nodePosition[i][1] = (0 + randomCoorY)
	randomCoorZ = uniform(-2, 4)
	nodePosition[i][2] = (13 + randomCoorZ + randomSize)
	print(randomCoorX)
	print(randomCoorY)
	print(randomCoorZ)
	bpy.ops.transform.translate(value = (randomCoorX, randomCoorY, randomCoorZ))
	"""

def createHouse(posX, posY):  
    cote = uniform(2,4)
    hauteur = cote#(cote*2)/3
    posZ = hauteur
    bpy.ops.mesh.primitive_cube_add(location = (posX, posY, posZ))  
    bpy.ops.transform.resize(value=(cote, cote, hauteur)) 
    #SET COLOR GREEN
    item = bpy.context.object
    #setMaterial('green', item)
    
def createLittleBuilding(posX, posY):
    cote = uniform(2,4)
    hauteur = cote*3
    posZ = hauteur
    bpy.ops.mesh.primitive_cube_add(location = (posX, posY, posZ))  
    bpy.ops.transform.resize(value=(cote, cote, hauteur)) 
    #SET COLOR pink 
    item = bpy.context.object
    #setMaterial('pink', item)    
    
def createBigBuilding(posX, posY):
    cote = uniform(2,4)
    hauteur = cote*5
    posZ = hauteur
    bpy.ops.mesh.primitive_cube_add(location = (posX, posY, posZ))  
    bpy.ops.transform.resize(value=(cote, cote, hauteur)) 
    #SET COLOR BLUE 
    item = bpy.context.object
    #setMaterial('blue', item)
    
def createTower(posX, posY):
    cote = uniform(2,4)
    hauteur = cote*10
    posZ = hauteur
    bpy.ops.mesh.primitive_cube_add(location = (posX, posY, posZ))  
    bpy.ops.transform.resize(value=(cote, cote, hauteur))
    #SET COLOR RED
    item = bpy.context.object   
    #setMaterial('red', item)
    
def setMaterial(color, item):
    mat = bpy.data.materials.new(color)
    if color == 'red':
        mat.diffuse_color = (1,0,0)
    elif color == 'green':
        mat.diffuse_color = (0,1,0)
    elif color =='blue':
        mat.diffuse_color = (0,0,1)
    elif color =='pink':
        mat.diffuse_color = (1,0,1)
    #mat.diffuse_shader = 'LAMBERT' 
    #mat.diffuse_intensity = 1.0 
    #mat.specular_color = (1,1,1)
    #mat.specular_shader = 'COOKTORR'
    #mat.specular_intensity = 0.5
    #mat.alpha = 1
    #mat.ambient = 1
    item.data.materials.append(mat)
    
#_________________________________________________#




