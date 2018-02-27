import bpy, config
from mathutils import Vector

class Camera:
	def __init__(self):
		self.cam = bpy.data.cameras.new("Camera")
		self.cam_ob = bpy.data.objects.new("Camera", self.cam)
		bpy.context.scene.objects.link(self.cam_ob)
	
		bpy.ops.object.select_all(action='DESELECT')

		self.cam_ob.select = True
		bpy.ops.transform.resize(value=(0.4,0.4,0.4))


		self.look_at_point = None
		self.camera_position = Vector((1,1,1))
		self.mode = 'free'

		if self.mode == 'free':
			self.init_free_mode()

	def toggle_camera(self):
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				override = bpy.context.copy()
				override['area'] = area
				bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
				break 

	def look_at(self, point):
		self.look_at_point = point
		loc_camera = self.cam_ob.location
		direction = point - loc_camera
		rot_quat = direction.to_track_quat('-Z', 'Y')
		self.cam_ob.rotation_euler = rot_quat.to_euler()

	def init_free_mode(self):
		if self.mode == 'free':
			self.look_at(Vector((0,0,0)))
			self.camera_position = Vector((0,0,20))			

	def switch_camera(self, robot,sys):
		if self.mode == 'free':
			self.adjust_camera()
		elif self.mode == 'inside':
			self.adjust_camera(type='inside', f_object=robot.data, position_vector = robot.act_walk.get_front_location(robot.data.dimensions,robot.data.location), direction_vector=config.direction_vector)
		elif self.mode == 'follow':
			self.adjust_camera(type='follow', f_object=robot.data)			

	def adjust_camera(self, type='free', f_object=None, position_vector=None, direction_vector=None):
		if type == 'free':
			self.look_at(Vector((0,0,0)))
			self.cam_ob.location = self.look_at_point + self.camera_position
		elif type == 'follow':
			self.cam_ob.location = f_object.location+Vector((1,1,1))
			self.look_at(f_object.location)
		elif type == 'inside':
			self.cam_ob.location = position_vector
			self.look_at(position_vector + direction_vector)
			