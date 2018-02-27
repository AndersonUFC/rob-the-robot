import Movement, mathutils, bpy,config, math, Actuator

class Rotate(Movement.Movement):
	def __init__(self, degree_rotation=math.pi/16):
		Movement.Movement.__init__(self)
		self.degree_rotation=degree_rotation

	def act(self, TYPE, robot, labirint, system):
		Actuator.last_action_state = TYPE
		bpy.ops.object.select_all(action='DESELECT')
		robot.data.select = True

		if TYPE == 'clockwise':
			config.direction_vector.rotate(mathutils.Euler((0,0,-self.degree_rotation),'XYZ'))
			bpy.ops.transform.rotate(value=-self.degree_rotation, axis=(0,0,1))

			if labirint.collide(system, system.get_BoundBox(robot.data.name)):			
				config.direction_vector.rotate(mathutils.Euler((0,0,self.degree_rotation),'XYZ'))
				bpy.ops.transform.rotate(value=self.degree_rotation, axis=(0,0,1))
				return True
			else:
				robot.act_mouth.girate(TYPE, self.degree_rotation)
		elif TYPE == 'counterclockwise':
			config.direction_vector.rotate(mathutils.Euler((0,0,self.degree_rotation),'XYZ'))
			bpy.ops.transform.rotate(value=self.degree_rotation, axis=(0,0,1))

			if labirint.collide(system, system.get_BoundBox(robot.data.name)):			
				config.direction_vector.rotate(mathutils.Euler((0,0,-self.degree_rotation),'XYZ'))
				bpy.ops.transform.rotate(value=-self.degree_rotation, axis=(0,0,1))
				return True
			else:
				robot.act_mouth.girate(TYPE, self.degree_rotation)
		
		return False