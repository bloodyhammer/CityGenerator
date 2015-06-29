from tools_blender import *

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
		
def set_uv_ground(nameMat, object, mesh, scalex, scaley):
	mat = createMaterial('img/' + nameMat)
	mat.specular_intensity = 0
	mat.texture_slots[0].texture_coords = 'UV'
	mat.texture_slots[0].scale[0] = scalex
	mat.texture_slots[0].scale[1] = scaley
	setMaterial(object, mat)
	
	mesh.faces[0].select = True	
	bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
	
def set_uv_balcon(nameMat, object, mesh, scalex, scaley):
	mat = createMaterial('img/' + nameMat)
	mat.specular_intensity = 0

	mat.texture_slots[0].texture_coords = 'UV'
	if object.name.startswith("Top") :
		mat.texture_slots[0].mapping = 'FLAT'
		mat.texture_slots[0].mapping_x = 'X'
		mat.texture_slots[0].mapping_y = 'Y'
		mat.texture_slots[0].mapping_z = 'X'		
	else :
		mat.texture_slots[0].mapping_x = 'X'
		mat.texture_slots[0].mapping_y = 'X'
		mat.texture_slots[0].mapping_z = 'Y'
	
	mat.texture_slots[0].scale[0] = scalex
	mat.texture_slots[0].scale[1] = scaley
	setMaterial(object, mat)
	
	mesh.faces[0].select = True	
	mesh.faces[1].select = True	
	mesh.faces[2].select = True	
	mesh.faces[3].select = True	
	mesh.faces[4].select = True
	bpy.ops.uv.cube_project(cube_size=20.0, correct_aspect=True, clip_to_bounds=True, scale_to_bounds=True)
	#bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)