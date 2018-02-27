import Actuator, bpy, math, bpy, config, mathutils

class Mouth(Actuator.Actuator):
	def __init__(self, robot_size):
		self.eated = False
		self.last_degree = 0.
		Actuator.Actuator.__init__(self)

		# create mouth
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.mesh.primitive_cube_add()
		bpy.ops.transform.resize(value=(robot_size*0.5, robot_size*1.5, robot_size*0.5))
		material = bpy.data.materials.new("reward material")
		material.diffuse_color = (0.1,0.1,0.1)
		bpy.context.object.data.materials.append(material)

		self.mouth = bpy.context.object
		#self.mouth.hide = True
		
		self.mouth.name = "mouth"

	def girate(self, direction, degree):
		bpy.ops.object.select_all(action='DESELECT')
		self.mouth.select = True

		if direction == 'clockwise':
			bpy.ops.transform.rotate(value=-degree, axis=(0,0,1))
		if direction == 'counterclockwise':
			bpy.ops.transform.rotate(value=degree, axis=(0,0,1))

	def act(self, TYPE, robot, labirint, system):

		# move mouth
		bpy.ops.object.select_all(action='DESELECT')
		self.mouth.select = True

		loc = self.mouth.location

		robot_bound_box = system.get_BoundBox(robot.data.name)
		front_loc = robot.act_walk.get_front_location(robot.data.dimensions, robot.data.location)

		bpy.ops.transform.translate(value=-loc)
		bpy.ops.transform.translate(value=front_loc)

		# detect -----------------------------------------------------------------------------
		mouth_bound_box = system.get_BoundBox(self.mouth.name)
		fruit, angle, distance = labirint.fruit_closer(system,robot_bound_box, front_loc)
		fruit_bound_box = system.get_BoundBox(fruit.data.name)

		collide1 = system.check_Collision(mouth_bound_box, fruit_bound_box)
		collide2 = system.check_Collision(fruit_bound_box, mouth_bound_box)

		col = collide1 or collide2
		
		if col and Actuator.last_action_state == 'foward':
			bpy.data.meshes.remove(fruit.data.data)
			bpy.data.objects.remove(fruit.data)   			
			labirint.fruits.remove(fruit)
			self.eated = True						
		else:
			self.eated = False