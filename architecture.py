import bpy
import bmesh

from random import *

from uv import *

def placeRessource(x, y, z, model, name):
	bpy.ops.object.select_all(action='TOGGLE')  
	bpy.ops.object.select_all(action='DESELECT')  
	bpy.context.scene.objects.active = bpy.data.objects[model]
	building = bpy.context.active_object
	building.select = True
	bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
	bpy.context.object.location[0] = x
	bpy.context.object.location[1] = y
	bpy.context.object.location[2] = z
	bpy.context.object.name = name
	bpy.ops.object.select_all(action='DESELECT')  

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
	
#Faire quelque chose pour ça 
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
	hauteur = cote*4
	
	#Building creation
	create_building('Big Building', posX, posY,  hauteur, cote)
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	#Texture building
	nbText = randint(1,4)
	nameMat = 'big' + str(nbText) + '.jpg'
	set_uv(nameMat, object, mesh,2,5)
	bpy.ops.object.mode_set(mode='OBJECT')
	object.location[0] = -2.5
	object.location[1] = -2.5
	
	#Top Building creation
	create_top_of_building('Top of Building', posX, posY, hauteur, cote)
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	#Texture top building
	set_uv('top_build_texture.jpg', object, mesh,2,5)
	
	bpy.ops.object.mode_set(mode='OBJECT')
	object.location[0] = -2.5
	object.location[1] = -2.5
	
def createTower(posX, posY):
	cote = uniform(4,5)
	hauteur = cote*6
	
	#Building creation
	create_building('Tower', posX, posY,  hauteur, cote)
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	#Texture building
	nbText = randint(1,4)
	nameMat = 'big' + str(nbText) + '.jpg'
	set_uv(nameMat, object, mesh,2,6)
	bpy.ops.object.mode_set(mode='OBJECT')
	object.location[0] = -2.5
	object.location[1] = -2.5
	
	#Top Building creation
	create_top_of_building('Top of Tower', posX, posY, hauteur, cote)
	object = bpy.context.active_object 
	obj_data = object.data
	bpy.ops.object.mode_set(mode='EDIT')
	mesh = bmesh.from_edit_mesh(obj_data)
	#Texture top building
	set_uv('top_build_texture.jpg', object, mesh,2,6)
	
	bpy.ops.object.mode_set(mode='OBJECT')
	object.location[0] = -2.5
	object.location[1] = -2.5
	
def create_top_of_building(name, px, py, hauteur, largeur):
	bpy.ops.object.select_all(action='TOGGLE')
	mesh = bpy.data.meshes.new(name="Mesh")
	topB_coords = []
	topB_faces = []
	pz = hauteur
	idx = 0
	
	create_top_coords(topB_coords,px, py, pz, hauteur, largeur)
	create_top_faces(topB_faces, idx)
	
	object = bpy.data.objects.new( name, mesh )
	#link de l'object à la scene
	bpy.context.scene.objects.link( object )
	mesh.from_pydata( topB_coords, [], topB_faces )
	mesh.update( calc_edges=True )
	bpy.context.scene.objects.active = object
	object.select = True
	
	return mesh, object	
	
def create_top_coords(topB_coords ,px, py, pz, hauteur, largeur):
	topB_coords.append(( px, py, pz ))
	topB_coords.append(( px + largeur, py, pz ))
	topB_coords.append(( px + largeur, py + largeur, pz ))
	topB_coords.append(( px, py+largeur , pz ))
	
	topB_coords.append(( px, py, pz + 1))
	topB_coords.append(( px + largeur, py, pz + 1))
	topB_coords.append(( px + largeur, py + largeur, pz + 1))
	topB_coords.append(( px, py+largeur , pz + 1))
	
	
	topB_coords.append(( px+0.25, py+0.25, pz +1))
	topB_coords.append(( px + largeur-0.25, py+0.25, pz+1 ))
	topB_coords.append(( px + largeur-0.25, py + largeur-0.25, pz+1 ))
	topB_coords.append(( px+0.25, py+largeur -0.25, pz+1 ))
	
	topB_coords.append(( px +0.25, py+0.25, pz + 0.5))
	topB_coords.append(( px + largeur-0.25, py+0.25, pz + 0.5))
	topB_coords.append(( px + largeur-0.25, py + largeur-0.25, pz + 0.5))
	topB_coords.append(( px+0.25, py+largeur -0.25, pz + 0.5))
	
def create_top_faces(topB_faces, idx):
	topB_faces.append(( idx, idx+1, idx+2, idx+3 ))
	
	topB_faces.append(( idx, idx+1, idx+5, idx+4 ))
	topB_faces.append(( idx+1, idx+2, idx+6, idx+5 ))
	topB_faces.append(( idx+2, idx+3, idx+7, idx+6 ))
	topB_faces.append(( idx+3, idx, idx+4, idx+7 ))
	
	topB_faces.append(( idx+4, idx+5, idx+9, idx+8 ))
	topB_faces.append(( idx+5, idx+6, idx+10, idx+9 ))
	topB_faces.append(( idx+6, idx+7, idx+11, idx+10 ))
	topB_faces.append(( idx+7, idx+4, idx+8, idx+11 ))
	
	topB_faces.append(( idx+12, idx+13, idx+9, idx+8 ))
	topB_faces.append(( idx+13, idx+14, idx+10, idx+9 ))
	topB_faces.append(( idx+14, idx+15, idx+11, idx+10 ))
	topB_faces.append(( idx+15, idx+12, idx+8, idx+11 ))
	
	topB_faces.append(( idx+12, idx+13, idx+14, idx+15 ))