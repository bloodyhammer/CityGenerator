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
		bpy.ops.object.mode_set(mode='OBJECT')
		for ob in bpy.context.scene.objects:
			ob.select = (ob.type == 'MESH' or ob.type == 'LAMP') and (ob.name.startswith("Cylinder") or ob.name.startswith("House") or ob.name.startswith("Little") or ob.name.startswith("Tower") or ob.name.startswith("Big")  or ob.name.startswith("Cube") or ob.name.startswith("Plane"))
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
	
	bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
	bpy.ops.transform.resize(value=(taille*4, taille*4, 0)) 
	

	#CREATE BUILDINGS
	#SET FLOOR
	bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
	bpy.ops.transform.resize(value=(taille, taille, 0)) 
	bpy.ops.transform.translate(value=(2.8, 1.6, 0), constraint_axis=(True, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)

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
			createTower(positionX, positionY) 
		elif (positionX >= -rangeLittleBuilding and positionX <= -rangeBigBuilding and positionY >= -rangeLittleBuilding and positionY <= rangeLittleBuilding) or (positionX >= rangeBigBuilding and positionX <= rangeLittleBuilding and positionY >= -rangeLittleBuilding and positionY <= rangeLittleBuilding) or (positionX >= -rangeLittleBuilding and positionX <= rangeLittleBuilding and positionY >= -rangeLittleBuilding and positionY <= -rangeBigBuilding) or (positionX >= -rangeLittleBuilding and positionX <= rangeLittleBuilding and positionY >= rangeBigBuilding and positionY <= rangeLittleBuilding) :
				createBigBuilding(positionX, positionY) 
		elif (positionX >= -rangeHouse and positionX <= -rangeLittleBuilding and positionY >= -rangeHouse and positionY <= rangeHouse) or (positionX >= rangeLittleBuilding and positionX <= rangeHouse and positionY >= -rangeHouse and positionY <= rangeHouse) or (positionX >= -rangeHouse and positionX <= rangeHouse and positionY >= -rangeHouse and positionY <= -rangeLittleBuilding) or (positionX >= -rangeHouse and positionX <= rangeHouse and positionY >= rangeLittleBuilding and positionY <= rangeHouse):
				createLittleBuilding(positionX, positionY)
		elif positionX <= -rangeHouse or positionX >= rangeHouse or positionY <= -rangeHouse or positionY >= rangeHouse:
			createHouse(positionX, positionY)
		i = i+1

	thick = 1.6
	random = uniform(0.1, 1)
	createPlaneRandom(taille*2 + margin, 0, taille, 0.125, thick)
	createPlaneRandom(0, taille*2 + margin, taille, 0.125, thick)
	createPlaneRandom(-taille*2, 0, taille, 0.125, thick)
	createPlaneRandom(0, -taille*2, taille, 0.125, thick)
	

def createPlaneRandom(x, y, taille, random, thick):
	bpy.ops.mesh.primitive_plane_add(location = (x, y, 0))
	bpy.ops.transform.resize(value=(taille, taille, 1)) 

	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.subdivide()
	bpy.ops.mesh.subdivide()
	bpy.ops.mesh.subdivide()
	bpy.ops.object.vertex_random(offset=random)

	bpy.ops.mesh.inset(thickness=0.035, use_select_inset=False, use_individual=True)

	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, uniform(10,15)), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
	bpy.ops.object.mode_set(mode='OBJECT')
	
def createHouse(posX, posY):  
	cote = uniform(4, 5)
	hauteur = cote * 2#(cote*2)/3
	mesh, object = create_building('House', posX, posY,  hauteur, cote)

	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	
	nbText = randint(1,4)
	nameMat = 'tower' + str(nbText) + '.jpg'
	set_uv(nameMat, object, mesh,2,2)
	
	bpy.ops.object.mode_set(mode='OBJECT')
		

def createLittleBuilding(posX, posY):
	cote = uniform(4,5)
	hauteur = cote*4
	create_building('Little Building', posX, posY,  hauteur, cote)
	
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	
	nbText = randint(1,4)
	nameMat = 'big' + str(nbText) + '.jpg'
	set_uv(nameMat, object, mesh,2,4)
	
	bpy.ops.object.mode_set(mode='OBJECT')
    
def createBigBuilding(posX, posY):
	cote = uniform(4,5)
	hauteur = cote*6
	create_building('Big Building', posX, posY,  hauteur, cote)
    
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	
	nbText = randint(1,4)
	nameMat = 'big' + str(nbText) + '.jpg'
	set_uv(nameMat, object, mesh,2,5)
	
	bpy.ops.object.mode_set(mode='OBJECT')
def createTower(posX, posY):
	cote = uniform(4,5)
	hauteur = cote*10
	create_building('Tower', posX, posY,  hauteur, cote)
	
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	
	nbText = randint(1,4)
	nameMat = 'tower' + str(nbText) + '.jpg'
	set_uv(nameMat, object, mesh,2,6)
	
	bpy.ops.object.mode_set(mode='OBJECT')

def create_cube_coords(coords,px, py, pz, hauteur, largeur):
	coords.append(( px, py, pz ))
	coords.append(( px + largeur, py, pz ))
	coords.append(( px + largeur, py + largeur, pz ))
	coords.append(( px, py+largeur , pz ))
	coords.append(( px, py, pz + hauteur))
	coords.append(( px + largeur, py, pz + hauteur))
	coords.append(( px + largeur, py + largeur, pz + hauteur))
	coords.append(( px, py+largeur , pz + hauteur))

def create_cube_faces(faces, idx):
	faces.append(( idx, idx+1, idx+2, idx+3 ))
	faces.append(( idx, idx+1, idx+5, idx+4 ))
	faces.append(( idx+1, idx+2, idx+6, idx+5 ))
	faces.append(( idx+2, idx+3, idx+7, idx+6 ))
	faces.append(( idx+3, idx, idx+4, idx+7 ))
	faces.append(( idx+4, idx+5, idx+6, idx+7 ))
	
def create_building(name, px, py, hauteur, largeur):
	bpy.ops.object.select_all(action='TOGGLE')

	mesh = bpy.data.meshes.new(name="Mesh")
	coords = []
	faces = []
	pz = 0
	idx = 0
	
	create_cube_coords(coords,px, py, pz, hauteur, largeur)
	create_cube_faces(faces, idx)

	object = bpy.data.objects.new( name, mesh )
	#link de l'object à la scene
	bpy.context.scene.objects.link( object )
	mesh.from_pydata( coords, [], faces )
	mesh.update( calc_edges=True )
	bpy.context.scene.objects.active = object
	object.select = True
	
	return mesh, object


def set_uv(nameMat, object, mesh, scalex, scaley):
	mat = createMaterial('img/' + nameMat)
	mat.specular_intensity = 0
	mat.texture_slots[0].texture_coords = 'UV'
	mat.texture_slots[0].scale[0] = scalex
	mat.texture_slots[0].scale[1] = scaley
	setMaterial(object, mat)
	
	mesh.faces[1].select = True	
	mesh.faces[2].select = True	
	mesh.faces[3].select = True	
	mesh.faces[4].select = True	
	bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    
def createMaterial(name):
	img = bpy.data.images.load('//'+name)
	tex = bpy.data.textures.new('TexName', type = 'IMAGE')
	tex.image = img
	mat = bpy.data.materials.new('MatName')
	
	ctex = mat.texture_slots.add()
	ctex.texture = tex
	ctex.texture_coords = 'UV'
	ctex.mapping = 'CUBE'
	return mat
	
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)




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
bpy.ops.transform.translate(value = (randomCoorX, randomCoorY, randomCoorZ))"""