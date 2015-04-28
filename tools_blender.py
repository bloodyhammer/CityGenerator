import bmesh
import random
import bpy

def createMaterial(name):
	img = bpy.data.images.load('//'+name)
	tex = bpy.data.textures.new('TexName', type = 'IMAGE')
	tex.image = img
	mat = bpy.data.materials.new('MatName')
	
	ctex = mat.texture_slots.add()
	ctex.texture = tex
	ctex.texture_coords = 'ORCO'
	ctex.mapping = 'CUBE'
	return mat

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
	
def print_index():
    mesh = bpy.context.object
    mesh_data = mesh.data
    mesh = bmesh.from_edit_mesh(mesh_data)
    i = 0
    for face in mesh.faces:
        if face.select == True:
            print(i)
        i = i + 1
    i = 0
	
def extrude_face(mesh, index, x, y, z):
    bpy.ops.mesh.select_all(action="DESELECT")
    mesh.faces[index].select = True
    axis_x = False
    axis_y = False
    axis_z = False
    if x != 0:
        axis_x = True
    if y != 0:
        axis_y = True
    if z != 0:
        axis_z = True
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(axis_x, axis_y, axis_z)})
	
    bpy.ops.mesh.select_all(action="DESELECT")  

def extrude_face_simple(mesh, x, y, z):
    axis_x = False
    axis_y = False
    axis_z = False
    if x != 0:
        axis_x = True
    if y != 0:
        axis_y = True
    if z != 0:
        axis_z = True
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(axis_x, axis_y, axis_z)})
	
    bpy.ops.mesh.select_all(action="DESELECT")  
	
def extrude_face_multiple(mesh, x, y, z, from_face, to_face):	
	bpy.ops.mesh.select_all(action="DESELECT")  
	mesh.faces[from_face].select = True
	mesh.faces[to_face].select = True
	bpy.ops.mesh.shortest_path_select()
	
	axis_x = False
	axis_y = False
	axis_z = False
	if x != 0:
		axis_x = True
	if y != 0:
		axis_y = True
	if z != 0:
		axis_z = True
	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(x, y, z), "constraint_axis":(axis_x, axis_y, axis_z)})
	bpy.ops.mesh.select_all(action="DESELECT")  
	
def translate_face(mesh, index, x, y, z):
    bpy.ops.mesh.select_all(action="DESELECT")
    mesh.faces[index].select = True
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  

def translate_edge(mesh, index, x, y, z):
    bpy.ops.mesh.select_all(action="DESELECT")
    mesh.verts[index].select = True
    bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  

def scale_face_contraint(mesh, index, x,y,z, value):
    bpy.ops.mesh.select_all(action="DESELECT")  
    mesh.faces[index].select = True
    bpy.ops.transform.resize(value=(value, value, value), constraint_axis=(x,y,z), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  

def scale_face(mesh, index, x,y,z):
    bpy.ops.mesh.select_all(action="DESELECT")  
    mesh.faces[index].select = True
    bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.mesh.select_all(action="DESELECT")  