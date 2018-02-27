# imports -------------------------------------------------------------------
import bpy, MainApplication, math, mathutils, config

# src -----------------------------------------------------------------------
class Labirint:
	def __init__(self, size_block_space=1, dimension_x=10, dimension_y=10):
		# member variables
		self.floor_x = dimension_x
		self.floor_y = dimension_y
		self.floor_center = 0
		self.size_block_space = size_block_space
		self.wall_path_ref = {}
		self.rewards = {}
		self.fruits = []
		self.fruits_backup = []
		self.matrix_ref_size = (self.floor_x*self.floor_y)/(self.size_block_space**2)
		self.wall_height = 0.2

	def create_floor(self):
		bpy.ops.mesh.primitive_plane_add()
		self.floor_ref = bpy.context.object
		material = bpy.data.materials.new("floor material")
		material.diffuse_color = (0.2,0.2,0.5)
		bpy.context.object.data.materials.append(material)
		bpy.ops.transform.resize(value=(self.floor_x*0.5,self.floor_y*0.5,1))
	
	def collide(self, system, robot_bb):
		for wpr in self.wall_path_ref:
		#for wpr in bpy.data.objects:
			#if "horizontal" in wpr.name or "vertical" in wpr.name:
			box = system.get_BoundBox(self.wall_path_ref[wpr].name)
			#box = system.get_BoundBox(wpr.name)

			collision1 = system.check_Collision(robot_bb, box)
			collision2 = system.check_Collision(box, robot_bb)
			if collision1 or collision2:
				return True
		return False

	def fruit_collide(self, system, robot_bb, robot_location):
		for fruit in self.fruits:
			box = system.get_BoundBox(fruit.data.name)

			collision1 = system.check_Collision(robot_bb, box)
			collision2 = system.check_Collision(box, robot_bb)

			if collision1 or collision2:
				vec = fruit.data.location - robot_location
				vec.z = 0

				vec = vec.normalized()*system.robot.act_walk.velocity

				bpy.ops.object.select_all(action='DESELECT')
				fruit.data.select = True				

				bpy.ops.transform.translate(value=vec)

				L2 = (fruit.data.location - mathutils.Vector((fruit.position_x, fruit.position_y, fruit.data.location.z))).length

				if self.collide(system, box):
					bpy.ops.transform.translate(value=-vec)					
					return True

				if L2 >= fruit.max_tension:
					rot_vec = (fruit.data.location - robot_location)
					rot_vec.z = 0
					rot_vec.rotate(mathutils.Euler((0,0,-math.pi/2),'XYZ'))
					rot_vec = rot_vec.normalized()*system.robot.act_walk.velocity

					bpy.ops.transform.translate(value=rot_vec)

		return False

	def fruit_closer(self, system, robot_bb, robot_location):
		closer_fruit = None
		min_angle = 9999
		min_distance = 9999

		for fruit in self.fruits:
			box = system.get_BoundBox(fruit.data.name)

			vec1 = (fruit.data.location - robot_location).normalized()
			vec2 = config.direction_vector.normalized()

			vec1.z = 0
			vec2.z = 0


			result_angle = math.acos(vec1 * vec2)

			result_dist = (fruit.data.location - robot_location)
			result_dist.z = 0

			result_dist = result_dist.length

			if result_dist < min_distance:
				min_distance = result_dist
				closer_fruit = fruit
				min_angle = result_angle

		return closer_fruit, min_angle, min_distance


	def add_wall(self, TYPE, dimension_x, dimension_y):
		bpy.ops.mesh.primitive_cube_add()
		
		#
		
		if TYPE == 'vertical':
			bpy.ops.transform.resize(value=(self.wall_width,self.size_block_space*0.5, self.wall_height))
			bpy.context.object.name = "vertical({},{})".format(dimension_x, dimension_y)	
			self.wall_path_ref[bpy.context.object.name] = bpy.context.object
			bpy.ops.transform.translate(value=((self.wall_width-self.floor_x)*0.5 + dimension_x*self.size_block_space,\
			                                    (self.size_block_space-self.floor_y)*0.5 + dimension_y*self.size_block_space,\
			                                    self.wall_height))			
			
		elif TYPE == 'horizontal':
			bpy.ops.transform.resize(value=(self.size_block_space*0.5, self.wall_width, self.wall_height))                    
			bpy.context.object.name = "horizontal({},{})".format(dimension_x, dimension_y)
			self.wall_path_ref[bpy.context.object.name] = bpy.context.object
			#bpy.ops.transform.rotate(value=math.pi/2, axis=(0,0,1))
			bpy.ops.transform.translate(value=((self.size_block_space-self.floor_x)*0.5 + dimension_x*self.size_block_space,\
			                                    (self.wall_width-self.floor_y)*0.5 + dimension_y*self.size_block_space,\
			                                    self.wall_height))			
		

		
	# getters -----------------------------------------------------------------------

	def get_floor_dimension(self):
		return self.floor_x, self.floor_y

	def get_size_block_space(self):
		return self.size_block_space
