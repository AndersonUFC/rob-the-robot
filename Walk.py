import Movement, mathutils, bpy, config, Actuator

class Walk(Movement.Movement):
	def __init__(self, velocity=0.01):
		Movement.Movement.__init__(self)
		self.velocity=velocity
		config.direction_vector = mathutils.Vector((0,self.velocity,0))

	def act(self, TYPE, robot, labirint, system):
		Actuator.last_action_state = TYPE
		bpy.ops.object.select_all(action='DESELECT')
		robot.data.select = True

		if TYPE == 'foward':
			bpy.ops.transform.translate(value=config.direction_vector)

			if labirint.collide(system, system.get_BoundBox(robot.data.name)):
				bpy.ops.transform.translate(value=-config.direction_vector)
				return True
			elif labirint.fruit_collide(system, system.get_BoundBox(robot.data.name), robot.data.location):
				bpy.ops.transform.translate(value=-config.direction_vector)
				return True
		elif TYPE == 'backward':
			bpy.ops.transform.translate(value=-config.direction_vector)
			
			if labirint.collide(system, system.get_BoundBox(robot.data.name)):
				bpy.ops.transform.translate(value=config.direction_vector)
				return True
			elif labirint.fruit_collide(system, system.get_BoundBox(robot.data.name), robot.data.location):
				bpy.ops.transform.translate(value=config.direction_vector)
				return True
		return False