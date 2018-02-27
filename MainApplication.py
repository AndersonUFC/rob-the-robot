# imports ------------------------
import bpy, threading, Labirint, mathutils, ManualLabirint, Robot, time, random, io_robot, Camera, ManualLabirintExamples, AutomaticLabirint, Display
import numpy as np

context = bpy.context

class MainApplication():
	def __init__(self):
		self.run()

	def run(self):
		print("Ta rodando heuiahuaehuahae\n")
		self.init_scenario()
		self.init_labirint()
		self.init_robot()
		self.init_camera()
		self.init_illumination()

		self.debug_txt = Display.Display()

		self.robot.brain.observe(self.robot, self.labirint, self)

		self.io_ = io_robot.IO_Robot()
		the_brain = self.io_.load_brain()

		not_load = True

		if the_brain:
			self.robot.brain = the_brain
			not_load = False
		self.camera.toggle_camera()
		self.camera.switch_camera(self.robot,self)

		
		#try:
		while True:
			self.robot.brain.observe(self.robot, self.labirint, self, not_load)
			not_load = False
			
			for i in range(0, 2000):	
				print(i)
				self.robot.brain.train(self.robot, self.labirint, self)					
				#self.robot.brain.predict(self.robot, self.labirint, self)
				
				self.camera.switch_camera(self.robot,self)
				self.deselect_objects()
				bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)	
				#self.save_images(i)
				self.put_fruits_back()

			self.io_.save_brain(self.robot)
			self.reset()	
		
		
	def save_images(self, timestep):
		for mode in ['free', 'inside','follow']:
				self.camera.mode = mode
				self.camera.switch_camera(self.robot,self)
				#bpy.data.scenes['Scene'].render.filepath = '//render/{}{}.png'.format(mode,timestep)
				#bpy.ops.render.render(write_still=True)
		self.camera.mode = 'free'
		self.camera.switch_camera(self.robot,self)
		
	def init_labirint(self):
		#self.labirint = ManualLabirintExamples.e1()
		self.labirint = AutomaticLabirint.AutomaticLabirint()
		
		# LOG ------------------------
		print("labirint initiated")

	def init_robot(self):
		self.robot = Robot.Robot(size=0.1)

		x,y = self.labirint.get_floor_dimension()
		space = self.labirint.get_size_block_space()
		self.robot.set_location((space-x)*0.5, (space-y)*0.5, 0.1)

		# LOG ------------------------

		print("robot initiated")		

	def init_scenario(self):
		# delete objects
		for obj in bpy.data.objects:
			bpy.data.objects.remove(obj)


		# delete meshes
		for mesh in bpy.data.meshes:
			bpy.data.meshes.remove(mesh)

		# reset cursor
		bpy.context.scene.cursor_location = mathutils.Vector((0,0,0))

		# LOG ------------------------
		print("scenario reseted")

	def reset(self):
		loc = self.robot.data.location
		self.robot.set_location(-loc.x,-loc.y,0)
		
		x,y = self.labirint.get_floor_dimension()
		space = self.labirint.get_size_block_space()		

		self.robot.set_location((space-x)*0.5, (space-y)*0.5, 0)

		self.labirint.reset_fruits()

	# system methods -----------------------------------------------------------
	def get_BoundBox(self, object_name):
		bpy.context.scene.update()
		ob = bpy.context.scene.objects[object_name]
		bbox_corners = [ob.matrix_world * mathutils.Vector(corner) for corner in ob.bound_box]

		del ob, object_name, self
		return bbox_corners	

	def check_Collision(self, box1, box2): 
		x_max = max([e[0] for e in box1])
		x_min = min([e[0] for e in box1])
		y_max = max([e[1] for e in box1])
		y_min = min([e[1] for e in box1])
		z_max = max([e[2] for e in box1])
		z_min = min([e[2] for e in box1])
		 
		x_max2 = max([e[0] for e in box2])
		x_min2 = min([e[0] for e in box2])
		y_max2 = max([e[1] for e in box2])
		y_min2 = min([e[1] for e in box2])
		z_max2 = max([e[2] for e in box2])
		z_min2 = min([e[2] for e in box2])
		 
		isColliding = ((x_max >= x_min2 and x_max <= x_max2) \
						or (x_min <= x_max2 and x_min >= x_min2)) \
						and ((y_max >= y_min2 and y_max <= y_max2) \
						or (y_min <= y_max2 and y_min >= y_min2)) \
						and ((z_max >= z_min2 and z_max <= z_max2) \
						or (z_min <= z_max2 and z_min >= z_min2))

		return isColliding



	# automatic methods --------------------------------------------------------
	def put_fruits_back(self):
		r_box = self.get_BoundBox(self.robot.data.name)

		
		for fruit in self.labirint.fruits:
			box = self.get_BoundBox(fruit.data.name)
			
			if not (self.check_Collision(r_box,box) or self.check_Collision(box,r_box)):		
				loc = fruit.data.location
				vec = (mathutils.Vector((fruit.position_x, fruit.position_y, loc.z))-loc) * 0.1
				self.deselect_objects()

				
				bpy.context.scene.objects.active = fruit.data
				fruit.data.select = True
				bpy.ops.transform.translate(value=vec)
				
				del loc, vec
			del box
		del r_box

	def deselect_objects(self):
		for obj in bpy.context.selected_objects:
			obj.select = False

	def init_illumination(self):
		x = self.labirint.floor_x/2
		y = self.labirint.floor_y/2

		bpy.ops.object.lamp_add(type='POINT')
		self.lamp1 = bpy.context.object
		self.lamp1.location = mathutils.Vector((0,0,5))

		bpy.ops.object.lamp_add(type='POINT')
		self.lamp2 = bpy.context.object
		self.lamp2.location = mathutils.Vector((x,y,5))

		bpy.ops.object.lamp_add(type='POINT')
		self.lamp3 = bpy.context.object
		self.lamp3.location = mathutils.Vector((-x,y,5))

		bpy.ops.object.lamp_add(type='POINT')
		self.lamp4 = bpy.context.object
		self.lamp4.location = mathutils.Vector((-x,-y,5))

		bpy.ops.object.lamp_add(type='POINT')
		self.lamp5 = bpy.context.object
		self.lamp5.location = mathutils.Vector((x,-y,5))

	def init_camera(self):
		self.camera = Camera.Camera()