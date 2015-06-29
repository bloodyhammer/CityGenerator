from random import *
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(bpy.data.filepath))
import bmesh
import bpy
from bpy.props import *
from math import *
 
from tools_blender import *
from architecture import *
from uv import *
 
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
		default = 50,
		min = 25,
		max = 100)
	bpy.types.Scene.LowPoly = BoolProperty(
		default = False,
        name = "LowPoly", 
        description = "Low Poly or not?")
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
		col.prop(scn, 'LowPoly', text = "lowpoly")
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
		
		lowPoly = bpy.context.scene.LowPoly
		if lowPoly == True:
			generate_town_alternative(taille, margin, valueHouse, valueLittle, valueBig)
		else:
			generate_town(taille, margin, valueHouse, valueLittle, valueBig)
		return{'FINISHED'}    

class OBJECT_OT_DeleteButton(bpy.types.Operator):
	bl_idname = "town.delete"
	bl_label = "Delete town"
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		for ob in bpy.context.scene.objects:
			ob.select = (ob.type == 'MESH' or ob.type == 'LAMP') and (ob.name.startswith("Cylinder") or ob.name.startswith("Top") or ob.name.startswith("Env") or ob.name.startswith("House") or ob.name.startswith("Little") or ob.name.startswith("Tower") or ob.name.startswith("Big")  or ob.name.startswith("Cube") or ob.name.startswith("Plane"))
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
	print("GENERATE TOWN")
	margin = 5
	cote = 5
	#BigPlane 
	"""bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0.1))
	bpy.ops.transform.resize(value=(taille*4, taille*4, 0)) """
	

	#CREATE BUILDINGS
	#SET FLOOR
	bpy.ops.mesh.primitive_plane_add(location = (0, 0, 0))
	bpy.ops.transform.resize(value=(taille, taille, 0)) 
	#

	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	nameMat = "road.jpg"
	set_uv_ground(nameMat, object, mesh,2,6)
	bpy.ops.object.mode_set(mode='OBJECT')

	#BUILDINGS POSITIONS
	x=- (taille - margin)
	y=- (taille - margin)
	
	realLargeur = (taille-margin)*2
	nbUnitPerCote = ceil((realLargeur / (margeBetweenBat + cote)) + 1);
	
	new_taille = ((margeBetweenBat + cote) * nbUnitPerCote)/2
	
	if(new_taille > realLargeur):
		bpy.context.object.scale[0] = new_taille
		bpy.context.object.scale[1] = new_taille
		
	nbBat = nbUnitPerCote * nbUnitPerCote;
	buildingPosTab = np.zeros((nbBat, 2), dtype='i')
	
	bpy.ops.transform.translate(value=((new_taille - taille)/2, (new_taille - taille)/2, 0), constraint_axis=(True, True, False))
	
	i=0
	for posNumX in range(0, int(nbBat/nbUnitPerCote)):
		for posNumY in range(0,int(nbBat/nbUnitPerCote)):                  
			buildingPosTab[i][0] = x
			buildingPosTab[i][1] = y
			i = i+1
			y = y+margeBetweenBat + cote
		y = -(taille - margin)
		x = x+margeBetweenBat + cote
	#print(buildingPosTab)

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
		randEnv = randint(0, 1)
		
		if positionX >= -rangeBigBuilding and positionX <= rangeBigBuilding and positionY >= -rangeBigBuilding and positionY <= rangeBigBuilding: 
			randBatiment = randint(0, 2)
			if(randBatiment == 0):
				createTower(positionX, positionY) 
			else:
				placeRessource(positionX, positionY, 0.1, "ModelHigh"+str(randBatiment), "Tower")
			
		elif (positionX >= -rangeLittleBuilding and positionX <= -rangeBigBuilding and positionY >= -rangeLittleBuilding and positionY <= rangeLittleBuilding) or (positionX >= rangeBigBuilding and positionX <= rangeLittleBuilding and positionY >= -rangeLittleBuilding and positionY <= rangeLittleBuilding) or (positionX >= -rangeLittleBuilding and positionX <= rangeLittleBuilding and positionY >= -rangeLittleBuilding and positionY <= -rangeBigBuilding) or (positionX >= -rangeLittleBuilding and positionX <= rangeLittleBuilding and positionY >= rangeBigBuilding and positionY <= rangeLittleBuilding) :
			randBatiment = randint(0, 1)
			if(randBatiment == 0):
				createBigBuilding(positionX, positionY) 
			else:
				placeRessource(positionX, positionY, 0.1, "ModelBig"+str(randBatiment), "BigBuilding")
				
		elif (positionX >= -rangeHouse and positionX <= -rangeLittleBuilding and positionY >= -rangeHouse and positionY <= rangeHouse) or (positionX >= rangeLittleBuilding and positionX <= rangeHouse and positionY >= -rangeHouse and positionY <= rangeHouse) or (positionX >= -rangeHouse and positionX <= rangeHouse and positionY >= -rangeHouse and positionY <= -rangeLittleBuilding) or (positionX >= -rangeHouse and positionX <= rangeHouse and positionY >= rangeLittleBuilding and positionY <= rangeHouse):
			randBatiment = randint(0, 3)
			placeRessource(positionX, positionY, 0.1 , "ModelHouse"+str(randBatiment), "LittleBuilding")
			if(randEnv == 0):
				placeRessource(positionX + cote/2, positionY + cote/2, 0, "Lamp", "Env")
			else:
				placeRessource(positionX + cote/2, positionY + cote/2, 0, "Tree", "Env")
		elif positionX <= -rangeHouse or positionX >= rangeHouse or positionY <= -rangeHouse or positionY >= rangeHouse:
			randBatiment = randint(0, 3)
			placeRessource(positionX, positionY, 0.1, "ModelHouse"+str(randBatiment), "House")
			if(randEnv == 0):
				placeRessource(positionX + cote/2, positionY + cote/2, 0, "Lamp", "Env")
			else:
				placeRessource(positionX + cote/2, positionY + cote/2, 0, "Tree", "Env")
		i = i+1

#def generate_town_alternative(taille, margeBetweenBat, valueHouse, valueLittle, valueBig):