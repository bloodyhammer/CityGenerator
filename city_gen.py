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
	bpy.types.Scene.Length = IntProperty(
		name = "Length", 
		description = "Enter an integer",
		default = 6,
		min = 5,
		max = 8)
	bpy.types.Scene.Taille = IntProperty(
		name = "Taille", 
		description = "Enter an integer",
		default = 3,
		min = 1,
		max = 6)
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
		row.alignment = 'EXPAND'
		row.prop(scn, 'Taille', text = "taille")
		
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
		lenght = bpy.context.scene.Length
		taille = bpy.context.scene.Taille
		generate_town(taille)
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


def generate_town(taille):
	taille = 170
	margin = 5
	margeBetweenBat = 10
	#CREATE BUILDINGS
	#SET FLOOR
	bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
	bpy.ops.transform.resize(value=(taille, taille, 0)) 

	#BUILDINGS POSITIONS
	nbBat = 1156
	buildingPosTab = np.zeros((nbBat, 2), dtype='i')
	x=- (taille - margin)
	y=- (taille - margin)
	i=0
	for posNumX in range(0,34):
		for posNumY in range(0,34): 
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
	#while i != 0:
	for buildNum in range(0,len(buildingPosTab)):
		#randPositionX = uniform(-50,50) 
		#randPositionY = uniform(-50,50) 
		positionX = buildingPosTab[i][0]
		positionY = buildingPosTab[i][1]
		#Centralisation des populations
		randBatiment = randint(0, 3)
		if positionX >= -45 and positionX <= 45 and positionY >= -45 and positionY <= 45:       
			#if randBatiment == 0:
			createTower(positionX, positionY) 
		elif (positionX >= -95 and positionX <= -55 and positionY >= -95 and positionY <= 95) or (positionX >= 55 and positionX <= 95 and positionY >= -95 and positionY <= 95) or (positionX >= -95 and positionX <= 95 and positionY >= -95 and positionY <= -55) or (positionX >= -95 and positionX <= 95 and positionY >= 55 and positionY <= 95) :
			#elif randBatiment == 1:
				createBigBuilding(positionX, positionY) 
		elif (positionX >= -135 and positionX <= -105 and positionY >= -135 and positionY <= 135) or (positionX >= 105 and positionX <= 135 and positionY >= -135 and positionY <= 135) or (positionX >= -135 and positionX <= 135 and positionY >= -135 and positionY <= -105) or (positionX >= -135 and positionX <= 135 and positionY >= 105 and positionY <= 135):
			#elif randBatiment == 2:
				createLittleBuilding(positionX, positionY)
		elif positionX <= -145 or positionX >= 145 or positionY <= -145 or positionY >= 145:
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




